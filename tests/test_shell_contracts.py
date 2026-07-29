import subprocess
import tempfile
import unittest
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ShellContractTests(unittest.TestCase):
    def test_sync_script_has_fail_fast_and_staging_guards(self):
        script = (REPO_ROOT / "scripts" / "sync-docs.sh").read_text(encoding="utf-8")

        self.assertIn("set -eu", script)
        self.assertIn("mktemp -d", script)
        self.assertNotIn('TEMP_DIR=".tmp_repo"', script)
        self.assertLess(script.index("validate_docs.py"), script.index('mv "$STAGED_DOCS"'))

    def test_installer_fails_for_nonempty_non_git_target(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "occupied"
            target.mkdir()
            (target / "user-file.txt").write_text("keep me", encoding="utf-8")

            result = subprocess.run(
                [
                    "bash",
                    str(REPO_ROOT / "scripts" / "install-skill.sh"),
                    str(target),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not an empty directory", result.stderr)

    def test_sync_failure_keeps_existing_snapshot(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            upstream = root / "upstream"
            skill_root = root / "skill"
            (upstream / "_pages").mkdir(parents=True)
            (upstream / "_includes" / "docs").mkdir(parents=True)
            (upstream / "_data").mkdir()
            (skill_root / "docs").mkdir(parents=True)
            sentinel = skill_root / "docs" / "keep.md"
            sentinel.write_text("existing snapshot", encoding="utf-8")

            (upstream / "_pages" / "page.md").write_text(
                "---\ntitle: Page\n---\n", encoding="utf-8"
            )
            (upstream / "_includes" / "docs" / "frontend_requirements.html").write_text(
                "<p>Requirements</p>\n", encoding="utf-8"
            )
            (upstream / "LICENSE.txt").write_text(
                "Apache License\n", encoding="utf-8"
            )
            subprocess.run(["git", "init", "-b", "develop"], cwd=upstream, check=True)
            subprocess.run(
                ["git", "config", "user.name", "Test"], cwd=upstream, check=True
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.com"],
                cwd=upstream,
                check=True,
            )
            subprocess.run(["git", "add", "."], cwd=upstream, check=True)
            subprocess.run(
                ["git", "commit", "-m", "test fixture"],
                cwd=upstream,
                check=True,
                capture_output=True,
            )

            environment = os.environ.copy()
            environment.update(
                {
                    "SPARTACUS_SKILL_ROOT": str(skill_root),
                    "SPARTACUS_UPSTREAM_REPO": str(upstream),
                    "SPARTACUS_MIN_DOC_COUNT": "1",
                    "SPARTACUS_FORCE_SYNC": "1",
                }
            )
            result = subprocess.run(
                ["sh", str(REPO_ROOT / "scripts" / "sync-docs.sh")],
                text=True,
                capture_output=True,
                check=False,
                env=environment,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "existing snapshot")
            self.assertFalse(any(skill_root.glob(".sync-work.*")))


if __name__ == "__main__":
    unittest.main()
