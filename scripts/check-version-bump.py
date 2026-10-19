#!/usr/bin/env python3
"""Fail when a plugin changes functionally without a version bump.

CI replacement for .claude/hooks/check-version-bump.sh, which only runs in a
local Claude session started in this repo. Implements the CLAUDE.md
"Version Management" rules over a commit range:

- A plugin whose functional files changed must raise `version` in
  plugins/<name>/.claude-plugin/plugin.json above the base version. A plugin
  that did not exist at the base passes (its first version is its bump).
- Any change to .claude-plugin/marketplace.json other than its version
  (adding or removing plugins, marketplace-level configuration) must raise
  `metadata.version` there.

Functional: anything under a plugin's skills/, commands/, agents/, hooks/,
lib/, scripts/, or .claude-plugin/ (other than plugin.json itself), its
.mcp.json, and code or JSON files anywhere in the plugin. Not functional:
README*, CHANGELOG*, docs/, disabled/, other top-level markdown or text.
Unlike the local hook, a SKILL.md or command .md edit counts as functional,
as CLAUDE.md requires.

Usage: check-version-bump.py [--base REF] [--head REF]
Exit: 0 pass, 1 missing bumps, 2 usage or git error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

FUNCTIONAL_DIRS = {"skills", "commands", "agents", "hooks", "lib", "scripts", ".claude-plugin"}
NON_FUNCTIONAL_DIRS = {"docs", "disabled"}
CODE_SUFFIXES = (".py", ".sh", ".js", ".mjs", ".cjs", ".ts", ".json")
MARKETPLACE = ".claude-plugin/marketplace.json"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(["git", *args], capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        print(f"error: git {' '.join(args)}: {result.stderr.strip()}", file=sys.stderr)
        raise SystemExit(2)
    return result


def read_json(ref: str, path: str) -> dict | None:
    result = git("show", f"{ref}:{path}", check=False)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        print(f"error: {ref}:{path} is not valid JSON: {error}", file=sys.stderr)
        raise SystemExit(2)


def semver(value: object) -> tuple[int, int, int] | None:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", str(value or "").strip())
    return tuple(int(part) for part in match.groups()) if match else None


def is_functional(rel: str) -> bool:
    """rel is the path inside plugins/<name>/."""
    parts = rel.split("/")
    if rel == ".claude-plugin/plugin.json":
        return False
    if parts[0] in NON_FUNCTIONAL_DIRS:
        return False
    if parts[0] in FUNCTIONAL_DIRS or rel == ".mcp.json":
        return True
    return rel.endswith(CODE_SUFFIXES)


def changed_plugins(paths: list[str]) -> set[str]:
    names = set()
    for path in paths:
        match = re.match(r"plugins/([^/]+)/(.+)$", path)
        if match and is_functional(match.group(2)):
            names.add(match.group(1))
    return names


def version_problem(base: str, head: str, plugin: str) -> str | None:
    path = f"plugins/{plugin}/.claude-plugin/plugin.json"
    new = read_json(head, path)
    if new is None:
        if git("cat-file", "-e", f"{head}:plugins/{plugin}", check=False).returncode != 0:
            return None  # plugin removed; the marketplace check covers it
        return f"{plugin}: {path} is missing"
    old = read_json(base, path)
    if old is None:
        return None if semver(new.get("version")) else f"{plugin}: version {new.get('version')!r} is not MAJOR.MINOR.PATCH"
    old_v, new_v = semver(old.get("version")), semver(new.get("version"))
    if new_v is None:
        return f"{plugin}: version {new.get('version')!r} is not MAJOR.MINOR.PATCH"
    if old_v is not None and new_v <= old_v:
        return f"{plugin}: functional changes but version {new.get('version')} is not above {old.get('version')}; bump {path}"
    return None


def marketplace_problem(base: str, head: str) -> str | None:
    old, new = read_json(base, MARKETPLACE) or {}, read_json(head, MARKETPLACE) or {}
    def config(doc: dict) -> str:
        doc = json.loads(json.dumps(doc))
        doc.get("metadata", {}).pop("version", None)
        return json.dumps(doc, sort_keys=True)

    if config(old) == config(new):
        return None
    old_v = semver(old.get("metadata", {}).get("version"))
    new_v = semver(new.get("metadata", {}).get("version"))
    if new_v is None or (old_v is not None and new_v <= old_v):
        return (
            f"marketplace: configuration changed but metadata.version "
            f"{new.get('metadata', {}).get('version')} is not above "
            f"{old.get('metadata', {}).get('version')}; bump {MARKETPLACE}"
        )
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    args = parser.parse_args()

    merge_base = git("merge-base", args.base, args.head).stdout.strip()
    # --no-renames: a skill moved between plugins changes both plugins.
    out = git("diff", "--name-only", "--no-renames", "-z", f"{merge_base}..{args.head}").stdout
    paths = [p for p in out.split("\0") if p]
    problems = [p for p in (version_problem(merge_base, args.head, name) for name in sorted(changed_plugins(paths))) if p]
    market = marketplace_problem(merge_base, args.head)
    if market:
        problems.append(market)

    if problems:
        print("VERSION BUMP REQUIRED (see CLAUDE.md 'Version Management'):")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print(f"check-version-bump: ok ({len(paths)} changed files, plugins changed: {', '.join(sorted(changed_plugins(paths))) or 'none'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
