#!/usr/bin/env python3
"""Run one of the genealogy clone's own Claude hooks in place.

Usage (from hooks/hooks.json):
    run-genealogy-hook.py <script-name>      # e.g. research-write-guard.py
    run-genealogy-hook.py --install-git-hooks

Cloud threads in a multi-repo project start above the clones, so
genealogy/.claude/settings.json never loads and its hooks never run. Copying
the scripts into this plugin would not help: they locate the repo by walking up
from the payload cwd, CLAUDE_PROJECT_DIR, or their own directory, and from the
plugin cache all three miss, so they exit 0 without doing anything.

This wrapper finds the genealogy clone itself and executes
<clone>/.claude/hooks/<script-name> at its real path, passing the hook payload
through unchanged and returning the script's stdout, stderr, and exit code. The
scripts stay single-sourced in the genealogy repo.

Fail-open like the scripts it wraps: if no clone is found, or the clone's own
settings.json already registers this script for the session's project
directory (a Mac session started inside the clone), it exits 0 silently.

Kill switch: GENEALOGY_GOVERNANCE_DISABLE=1. Override the clone location with
GENEALOGY_REPO_DIR. Each invocation appends one line to
$XDG_STATE_HOME/genealogy-governance/hooks.log (default ~/.local/state/...) so
a thread can confirm the hooks fired.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

INTERPRETERS = {".py": ["python3"], ".mjs": ["node"], ".js": ["node"], ".sh": ["bash"]}


def is_genealogy_root(path: Path) -> bool:
    return (
        (path / "AGENTS.md").is_file()
        and (path / "governance" / "codes").is_dir()
        and (path / ".claude" / "hooks").is_dir()
    )


def find_clone(starts: list[str]) -> Path | None:
    """Walk up from each start; at each level try the dir and its genealogy/ child."""
    for start in starts:
        if not start or not os.path.isdir(start):
            continue
        current = Path(start).resolve()
        while True:
            for candidate in (current, current / "genealogy"):
                if is_genealogy_root(candidate):
                    return candidate
            if current.parent == current:
                break
            current = current.parent
    return None


def settings_already_run(clone: Path, script: str) -> bool:
    """True when the session's project dir is the clone and its settings register the script."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir or not os.path.isdir(project_dir):
        return False
    if Path(project_dir).resolve() != clone:
        return False
    try:
        settings = (clone / ".claude" / "settings.json").read_text(encoding="utf-8")
    except OSError:
        return False
    return f".claude/hooks/{script}" in settings


def log(event: str, target: str, clone: Path | None, outcome: str) -> None:
    try:
        state = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local" / "state")
        log_dir = state / "genealogy-governance"
        log_dir.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        with open(log_dir / "hooks.log", "a", encoding="utf-8") as handle:
            handle.write(f"{stamp}\t{event}\t{target}\t{clone or '-'}\t{outcome}\n")
    except OSError:
        pass


def install_git_hooks(clone: Path, event: str) -> int:
    """Install the clone's pre-commit export guard; speak only on failure."""
    installer = clone / "scripts" / "install-git-hooks.sh"
    if not installer.is_file():
        log(event, "--install-git-hooks", clone, "installer-missing")
        print(
            "genealogy-governance: pre-commit export guard NOT installed: "
            f"{installer} is missing (needs the genealogy change that adds it). "
            "Run `python3 scripts/check-tree-exports.py` before each commit."
        )
        return 0
    try:
        result = subprocess.run(
            ["bash", str(installer)], cwd=clone, capture_output=True, text=True, check=False
        )
    except OSError as error:
        log(event, "--install-git-hooks", clone, f"spawn-failed={type(error).__name__}")
        print(f"genealogy-governance: pre-commit export guard NOT installed: {error}")
        return 0
    log(event, "--install-git-hooks", clone, f"exit={result.returncode}")
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        print(f"genealogy-governance: pre-commit export guard NOT installed: {detail}")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: run-genealogy-hook.py <script-name>|--install-git-hooks", file=sys.stderr)
        return 0
    target = sys.argv[1]
    payload = sys.stdin.buffer.read()
    try:
        data = json.loads(payload or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = {}
    event = data.get("hook_event_name", "?") if isinstance(data, dict) else "?"
    payload_cwd = data.get("cwd", "") if isinstance(data, dict) else ""

    if os.environ.get("GENEALOGY_GOVERNANCE_DISABLE") == "1":
        log(event, target, None, "disabled")
        return 0

    clone = find_clone(
        [
            os.environ.get("GENEALOGY_REPO_DIR", ""),
            payload_cwd if isinstance(payload_cwd, str) else "",
            os.environ.get("CLAUDE_PROJECT_DIR", ""),
            os.getcwd(),
        ]
    )
    if clone is None:
        log(event, target, None, "no-clone")
        return 0

    if target == "--install-git-hooks":
        return install_git_hooks(clone, event)

    if "/" in target or target.startswith("."):
        log(event, target, clone, "bad-name")
        return 0
    script = clone / ".claude" / "hooks" / target
    if not script.is_file():
        log(event, target, clone, "script-missing")
        return 0
    if settings_already_run(clone, target):
        log(event, target, clone, "skipped-settings-active")
        return 0

    command = INTERPRETERS.get(script.suffix, []) + [str(script)]
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(clone))
    try:
        result = subprocess.run(command, input=payload, cwd=clone, env=env, capture_output=True, check=False)
    except OSError as error:
        log(event, target, clone, f"spawn-failed={type(error).__name__}")
        return 0
    sys.stdout.buffer.write(result.stdout)
    sys.stderr.buffer.write(result.stderr)
    log(event, target, clone, f"exit={result.returncode}")
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
