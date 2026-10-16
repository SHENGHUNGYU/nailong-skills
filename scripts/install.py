#!/usr/bin/env python3
"""Install complete skill folders into an agent's documented discovery path."""

import argparse
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid


# Paths and invocation details are sourced in docs/agent-compatibility.md.
AGENTS = {
    "codex": (".agents/skills", ".agents/skills"),
    "claude-code": (".claude/skills", ".claude/skills"),
    "cursor": (".cursor/skills", ".cursor/skills"),
    "copilot": (".github/skills", ".copilot/skills"),
    "gemini-cli": (".gemini/skills", ".gemini/skills"),
    "windsurf": (".windsurf/skills", ".codeium/windsurf/skills"),
    "opencode": (".opencode/skills", ".config/opencode/skills"),
}


def destination(agent, scope, project=None):
    project_path, user_path = AGENTS[agent]
    if scope == "project":
        if project is None or not project.is_dir():
            raise ValueError("--scope project requires --project pointing to an existing directory")
        return project.expanduser().resolve() / project_path
    if agent == "opencode":
        config = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
        if not config.is_absolute():
            raise ValueError("XDG_CONFIG_HOME must be an absolute path")
        return config / "opencode/skills"
    return Path.home() / user_path


def install(source_root, target_root, names, force=False, dry_run=False):
    available = {p.name: p for p in source_root.iterdir()
                 if p.is_dir() and not p.is_symlink() and (p / "SKILL.md").is_file()}
    selected = list(dict.fromkeys(names or sorted(available)))
    if not selected:
        raise ValueError("No skill folders containing SKILL.md found")
    unknown = set(selected) - set(available)
    if unknown:
        raise ValueError("Unknown skill(s): " + ", ".join(sorted(unknown)))
    plans = []
    # Preflight every requested skill before making any filesystem changes.
    for name in selected:
        source = available[name].resolve()
        target = target_root / name
        resolved = target.resolve()
        if source == resolved or source in resolved.parents or resolved in source.parents:
            raise ValueError("Source and destination overlap: " + str(target))
        # Do not redirect installation through a symlinked parent or destination.
        if any(p.is_symlink() for p in (target, *target.parents)):
            raise ValueError("Destination contains a symlink: " + str(target))
        if any(p.is_symlink() for p in source.rglob("*")):
            raise ValueError("Skill contains a symlink: " + name)
        if target.exists() and not force:
            raise FileExistsError(str(target) + " already exists; use --force to back it up and replace it")
        plans.append((source, target))
    for source, target in plans:
        print(("Would install " if dry_run else "Installing ") + str(source) + " -> " + str(target))
        if dry_run:
            continue
        target_root.mkdir(parents=True, exist_ok=True)
        backup = None
        # Stage the complete folder on the same filesystem before replacing anything.
        with tempfile.TemporaryDirectory(prefix=".nailong-install-", dir=target_root) as temp:
            staged = Path(temp) / source.name
            shutil.copytree(source, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", ".git"))
            if target.exists():
                backup = target.with_name(target.name + ".backup-" + uuid.uuid4().hex)
                # Backups must be outside the discovery directory to avoid duplicate skills.
                backup_dir = target_root.parent / "nailong-skills-backups"
                if backup_dir.is_symlink():
                    raise ValueError("Backup directory is a symlink: " + str(backup_dir))
                backup_dir.mkdir(exist_ok=True)
                backup = backup_dir / backup.name
                target.rename(backup)
            try:
                staged.rename(target)
            except OSError:
                if backup is not None:
                    backup.rename(target)
                raise
        if backup is not None:
            print("Backup: " + str(backup))
    return len(plans)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", choices=sorted(AGENTS), required=True)
    parser.add_argument("--scope", choices=("user", "project"), default="user")
    parser.add_argument("--project", type=lambda s: Path(s).expanduser(), help="existing project directory; required for project scope")
    parser.add_argument("--skill", action="append", help="skill folder name; repeat to select several; default: all")
    parser.add_argument("--dry-run", action="store_true", help="print and validate the plan without writing files")
    parser.add_argument("--force", action="store_true", help="back up and replace existing skill folders")
    args = parser.parse_args(argv)
    if args.project is not None and args.scope != "project":
        parser.error("--project is only valid with --scope project")
    try:
        root = Path(__file__).resolve().parents[1]
        target = destination(args.agent, args.scope, args.project)
        count = install(root, target, args.skill, args.force, args.dry_run)
    except (OSError, ValueError) as error:
        print("Error: " + str(error), file=sys.stderr)
        return 1
    print(("Planned " if args.dry_run else "Installed ") + str(count) + " skill(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
