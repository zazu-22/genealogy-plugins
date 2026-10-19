"""Tests for scripts/check-version-bump.py against throwaway git repos."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check-version-bump.py"


class CheckVersionBumpTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "t@example.com")
        self.git("config", "user.name", "t")
        self.write_plugin("alpha", "1.0.0")
        self.write("plugins/alpha/skills/a/SKILL.md", "v1\n")
        self.write_marketplace("0.1.0", ["alpha"])
        self.commit("base")
        self.git("checkout", "-q", "-b", "feature")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(["git", *args], cwd=self.repo, capture_output=True, text=True, check=True).stdout

    def write(self, rel: str, text: str) -> None:
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def write_plugin(self, name: str, version: str) -> None:
        self.write(f"plugins/{name}/.claude-plugin/plugin.json", json.dumps({"name": name, "version": version}))

    def write_marketplace(self, version: str, names: list[str]) -> None:
        doc = {"metadata": {"version": version}, "plugins": [{"name": n, "source": f"./plugins/{n}"} for n in names]}
        self.write(".claude-plugin/marketplace.json", json.dumps(doc))

    def commit(self, message: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-qm", message)

    def check(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["python3", str(SCRIPT), "--base", "main", "--head", "HEAD"],
            cwd=self.repo, capture_output=True, text=True, check=False,
        )

    def test_skill_markdown_change_without_bump_fails(self) -> None:
        self.write("plugins/alpha/skills/a/SKILL.md", "v2\n")
        self.commit("edit skill")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("alpha", result.stdout)

    def test_bump_later_in_the_range_passes(self) -> None:
        self.write("plugins/alpha/skills/a/SKILL.md", "v2\n")
        self.commit("edit skill")
        self.write_plugin("alpha", "1.0.1")
        self.commit("bump")
        self.assertEqual(self.check().returncode, 0)

    def test_version_must_increase_not_just_change(self) -> None:
        self.write("plugins/alpha/hooks/hooks.json", "{}")
        self.write_plugin("alpha", "0.9.0")
        self.commit("downgrade")
        self.assertEqual(self.check().returncode, 1)

    def test_docs_and_readme_and_disabled_do_not_need_bump(self) -> None:
        self.write("plugins/alpha/README.md", "readme\n")
        self.write("plugins/alpha/docs/notes.md", "notes\n")
        self.write("plugins/alpha/disabled/old.py", "print()\n")
        self.write("docs/x.md", "x\n")
        self.commit("docs")
        self.assertEqual(self.check().returncode, 0)

    def test_skill_moved_between_plugins_flags_both(self) -> None:
        self.write_plugin("beta", "1.0.0")
        self.write("plugins/beta/hooks/hooks.json", "{}")
        self.write_marketplace("0.1.0", ["alpha", "beta"])
        self.git("add", "-A")
        self.git("commit", "-qm", "beta")
        self.git("branch", "-f", "main")
        (self.repo / "plugins/beta/skills").mkdir(parents=True)
        self.git("mv", "plugins/alpha/skills/a", "plugins/beta/skills/a")
        self.write_plugin("beta", "1.1.0")
        self.commit("move skill")
        result = self.check()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("alpha", result.stdout)

    def test_new_plugin_requires_marketplace_bump(self) -> None:
        self.write_plugin("beta", "0.1.0")
        self.write("plugins/beta/hooks/hooks.json", "{}")
        self.write_marketplace("0.1.0", ["alpha", "beta"])
        self.commit("add beta")
        result = self.check()
        self.assertEqual(result.returncode, 1)
        self.assertIn("marketplace", result.stdout)
        self.write_marketplace("0.2.0", ["alpha", "beta"])
        self.commit("bump marketplace")
        self.assertEqual(self.check().returncode, 0)


if __name__ == "__main__":
    unittest.main()
