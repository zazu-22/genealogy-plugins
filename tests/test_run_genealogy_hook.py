"""Tests for plugins/genealogy-governance/scripts/run-genealogy-hook.py.

Each test builds a fake workspace shaped like a multi-repo cloud thread
(a parent directory holding a genealogy/ clone) with stub hook scripts, then
runs the wrapper the way hooks.json does.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

WRAPPER = Path(__file__).resolve().parents[1] / "plugins/genealogy-governance/scripts/run-genealogy-hook.py"


def make_clone(root: Path) -> Path:
    clone = root / "genealogy"
    (clone / "governance" / "codes").mkdir(parents=True)
    (clone / ".claude" / "hooks").mkdir(parents=True)
    (clone / "AGENTS.md").write_text("# AGENTS.md\n")
    echo = clone / ".claude" / "hooks" / "echo.py"
    echo.write_text(
        "import json, os, sys\n"
        "data = json.load(sys.stdin)\n"
        "print(json.dumps({'cwd': data.get('cwd'), 'proc_cwd': os.getcwd(),"
        " 'project_dir': os.environ.get('CLAUDE_PROJECT_DIR')}))\n"
    )
    block = clone / ".claude" / "hooks" / "block.sh"
    block.write_text("#!/bin/bash\necho blocked >&2\nexit 2\n")
    return clone


class RunGenealogyHookTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.clone = make_clone(self.root)
        self.env = dict(os.environ, XDG_STATE_HOME=str(self.root / "state"), CLAUDE_PROJECT_DIR=str(self.root))
        self.env.pop("GENEALOGY_REPO_DIR", None)
        self.env.pop("GENEALOGY_GOVERNANCE_DISABLE", None)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_wrapper(self, target: str, payload: dict, **env: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["python3", str(WRAPPER), target],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            cwd=self.root,
            env={**self.env, **env},
            check=False,
        )

    def log_lines(self) -> list[str]:
        path = self.root / "state" / "genealogy-governance" / "hooks.log"
        return path.read_text().splitlines() if path.exists() else []

    def test_finds_child_clone_from_parent_cwd_and_passes_payload_unchanged(self) -> None:
        result = self.run_wrapper("echo.py", {"hook_event_name": "SessionStart", "cwd": str(self.root)})
        self.assertEqual(result.returncode, 0, result.stderr)
        out = json.loads(result.stdout)
        self.assertEqual(out["cwd"], str(self.root))  # payload untouched
        self.assertEqual(out["proc_cwd"], str(self.clone))
        self.assertEqual(out["project_dir"], str(self.clone))
        self.assertIn("exit=0", self.log_lines()[-1])

    def test_finds_clone_from_sibling_repo_cwd(self) -> None:
        sibling = self.root / "genealogy-plugins" / "plugins"
        sibling.mkdir(parents=True)
        result = self.run_wrapper("echo.py", {"cwd": str(sibling)}, CLAUDE_PROJECT_DIR=str(sibling))
        self.assertEqual(json.loads(result.stdout)["proc_cwd"], str(self.clone))

    def test_propagates_blocking_exit_code_and_stderr(self) -> None:
        result = self.run_wrapper("block.sh", {"hook_event_name": "TaskCompleted", "cwd": str(self.root)})
        self.assertEqual(result.returncode, 2)
        self.assertIn("blocked", result.stderr)

    def test_no_clone_is_silent_success(self) -> None:
        elsewhere = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, elsewhere, True)
        result = subprocess.run(
            ["python3", str(WRAPPER), "echo.py"],
            input=json.dumps({"cwd": elsewhere}),
            capture_output=True, text=True, cwd=elsewhere,
            env={**self.env, "CLAUDE_PROJECT_DIR": elsewhere}, check=False,
        )
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_skips_when_clone_settings_already_register_the_script(self) -> None:
        (self.clone / ".claude" / "settings.json").write_text(
            '{"hooks": {"x": [{"command": "\\"$CLAUDE_PROJECT_DIR\\"/.claude/hooks/echo.py"}]}}'
        )
        result = self.run_wrapper("echo.py", {"cwd": str(self.clone)}, CLAUDE_PROJECT_DIR=str(self.clone))
        self.assertEqual((result.returncode, result.stdout), (0, ""))
        self.assertIn("skipped-settings-active", self.log_lines()[-1])

    def test_kill_switch(self) -> None:
        result = self.run_wrapper("block.sh", {"cwd": str(self.root)}, GENEALOGY_GOVERNANCE_DISABLE="1")
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_rejects_path_traversal(self) -> None:
        result = self.run_wrapper("../../AGENTS.md", {"cwd": str(self.root)})
        self.assertEqual((result.returncode, result.stdout), (0, ""))
        self.assertIn("bad-name", self.log_lines()[-1])

    def test_install_reports_missing_installer(self) -> None:
        result = self.run_wrapper("--install-git-hooks", {"cwd": str(self.root)})
        self.assertEqual(result.returncode, 0)
        self.assertIn("NOT installed", result.stdout)

    def test_install_runs_clone_installer_quietly(self) -> None:
        scripts = self.clone / "scripts"
        scripts.mkdir()
        (scripts / "install-git-hooks.sh").write_text("#!/bin/bash\necho installed\n")
        result = self.run_wrapper("--install-git-hooks", {"cwd": str(self.root)})
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_install_reports_failed_installer(self) -> None:
        scripts = self.clone / "scripts"
        scripts.mkdir()
        (scripts / "install-git-hooks.sh").write_text("#!/bin/bash\necho installer failed >&2\nexit 1\n")
        result = self.run_wrapper("--install-git-hooks", {"cwd": str(self.root)})
        self.assertEqual(result.returncode, 0)
        self.assertIn("NOT installed", result.stdout)
        self.assertIn("installer failed", result.stdout)

    def test_missing_interpreter_fails_open(self) -> None:
        (self.clone / ".claude" / "hooks" / "noexec.bin").write_text("data\n")  # no interpreter, no +x
        result = self.run_wrapper("noexec.bin", {"cwd": str(self.root)})
        self.assertEqual((result.returncode, result.stdout), (0, ""))
        self.assertIn("spawn-failed=PermissionError", self.log_lines()[-1])


if __name__ == "__main__":
    unittest.main()
