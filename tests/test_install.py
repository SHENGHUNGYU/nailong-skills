import contextlib
import importlib.util
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "repo"
        self.skill = self.source / "example"
        (self.skill / "references").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("example", encoding="utf-8")
        (self.skill / "references/facts.md").write_text("facts", encoding="utf-8")
        self.target = self.root / "project/.agents/skills"

    def install(self, names=None, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return installer.install(self.source, self.target, names, **kwargs)

    def test_copy_complete_folder_and_select(self):
        self.assertEqual(self.install(["example", "example"]), 1)
        self.assertEqual((self.target / "example/references/facts.md").read_text(), "facts")
        self.assertEqual((self.skill / "SKILL.md").read_text(), "example")

    def test_dry_run_has_no_writes(self):
        self.install(dry_run=True)
        self.assertFalse(self.target.parent.exists())

    def test_conflict_preserves_existing(self):
        self.install()
        (self.target / "example/SKILL.md").write_text("local edits")
        with self.assertRaises(FileExistsError):
            self.install()
        self.assertEqual((self.target / "example/SKILL.md").read_text(), "local edits")

    def test_force_backups_outside_discovery(self):
        self.install()
        (self.target / "example/SKILL.md").write_text("local edits")
        self.install(force=True)
        backups = list((self.target.parent / "nailong-skills-backups").glob("example.backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / "SKILL.md").read_text(), "local edits")
        self.assertEqual([p.name for p in self.target.iterdir()], ["example"])

    def test_unknown_and_traversal_rejected_before_writes(self):
        for name in ["missing", "../example", str(self.skill)]:
            with self.assertRaises(ValueError):
                self.install(["example", name])
        self.assertFalse(self.target.exists())

    def test_overlap_rejected(self):
        for target in [self.source, self.skill / "nested"]:
            with self.assertRaises(ValueError):
                installer.install(self.source, target, ["example"], force=True)

    @unittest.skipIf(os.name == "nt", "symlinks can require Windows privileges")
    def test_destination_symlink_rejected(self):
        other = self.root / "other"
        other.mkdir()
        self.target.parent.mkdir(parents=True)
        self.target.symlink_to(other, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.install()
        self.assertEqual(list(other.iterdir()), [])

    @unittest.skipIf(os.name == "nt", "symlinks can require Windows privileges")
    def test_source_symlink_rejected(self):
        (self.skill / "linked").symlink_to(self.skill / "SKILL.md")
        with self.assertRaises(ValueError):
            self.install()

    def test_copy_failure_preserves_existing(self):
        self.install()
        (self.target / "example/SKILL.md").write_text("keep")
        with patch.object(installer.shutil, "copytree", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                self.install(force=True)
        self.assertEqual((self.target / "example/SKILL.md").read_text(), "keep")

    def test_replacement_failure_restores_backup(self):
        self.install()
        (self.target / "example/SKILL.md").write_text("keep")
        rename = Path.rename

        def fail_staged(path, target):
            if path.parent.name.startswith(".nailong-install-"):
                raise OSError("replacement failed")
            return rename(path, target)

        with patch.object(Path, "rename", fail_staged):
            with self.assertRaises(OSError):
                self.install(force=True)
        self.assertEqual((self.target / "example/SKILL.md").read_text(), "keep")

    def test_preflight_conflict_prevents_other_installs(self):
        other = self.source / "second"
        other.mkdir()
        (other / "SKILL.md").write_text("second")
        (self.target / "second").mkdir(parents=True)
        with self.assertRaises(FileExistsError):
            self.install(["example", "second"])
        self.assertFalse((self.target / "example").exists())

    def test_project_destinations(self):
        project = self.root / "a project"
        project.mkdir()
        expected = {
            "codex": ".agents/skills", "claude-code": ".claude/skills",
            "cursor": ".cursor/skills", "copilot": ".github/skills",
            "gemini-cli": ".gemini/skills", "windsurf": ".windsurf/skills",
            "opencode": ".opencode/skills",
        }
        for agent, suffix in expected.items():
            dest = installer.destination(agent, "project", project)
            self.assertEqual(dest, project / suffix)
            with contextlib.redirect_stdout(io.StringIO()):
                installer.install(self.source, dest, ["example"], dry_run=True)

    def test_user_destinations_and_xdg(self):
        with patch.object(installer.Path, "home", return_value=self.root), patch.dict(os.environ, {"XDG_CONFIG_HOME": ""}):
            for agent, (_, suffix) in installer.AGENTS.items():
                self.assertEqual(installer.destination(agent, "user"), self.root / suffix)
            with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(self.root / "xdg")}):
                self.assertEqual(installer.destination("opencode", "user"), self.root / "xdg/opencode/skills")

    def test_project_required(self):
        for project in [None, self.root / "missing"]:
            with self.assertRaises(ValueError):
                installer.destination("codex", "project", project)


if __name__ == "__main__":
    unittest.main()
