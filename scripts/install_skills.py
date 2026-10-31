#!/usr/bin/env python3
"""Install or export agent-specific skills without overwriting existing data."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
from edition_tools import ROOT, copy_skill, profiles


def main() -> int:
    root = ROOT
    catalog = json.loads((root / "skills.json").read_text(encoding="utf-8"))
    entries = {entry["name"]: entry for entry in catalog["skills"]}
    hosts = profiles()
    packaged = root / 'edition.json'
    default_agent = json.loads(packaged.read_text())['agent'] if packaged.is_file() else 'codex'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', choices=hosts, default=default_agent)
    parser.add_argument('--all', action='store_true', help='Select all skills')
    parser.add_argument("--skill", action="append", choices=sorted(entries), help="Repeat to select multiple skills")
    parser.add_argument("--dest", type=Path, help="Explicit skill or export directory")
    parser.add_argument('--project', type=Path, help='Install to this project using the selected agent layout')
    parser.add_argument("--dry-run", action="store_true", help="Show the plan without writing files")
    args = parser.parse_args()
    if args.dest and args.project:
        parser.error('Choose --dest or --project, not both')
    selected = list(entries) if args.all else list(dict.fromkeys(args.skill or []))
    if not selected:
        parser.print_help()
        return 0

    profile = hosts[args.agent]
    if args.dest:
        destination = args.dest.expanduser().resolve()
    elif args.project:
        if profile['mode'] != 'local':
            parser.error('This edition is imported or used in chat; provide --dest to export it')
        destination = args.project.expanduser().resolve().joinpath(*profile['project_parts'])
    elif profile['mode'] == 'local':
        if args.agent == 'deepseek-harness' and os.environ.get('DSH_HOME'):
            destination = Path(os.environ['DSH_HOME']).expanduser().resolve() / 'skills'
        else:
            destination = Path.home().joinpath(*profile['home_parts']).resolve()
    else:
        destination = (Path.cwd() / 'agent-exports' / args.agent).resolve()
    plan = []
    for name in selected:
        source = (root / entries[name]["path"]).resolve()
        target = destination / name
        if not source.is_relative_to(root / "skills") or not (source / "SKILL.md").is_file():
            parser.error(f"Invalid skill source: {name}")
        if target == source or target.is_relative_to(source) or source.is_relative_to(target):
            parser.error(f"Source and destination overlap: {name}")
        if target.exists() or target.is_symlink():
            parser.error(f"Destination already exists; choose another location or back it up first: {target}")
        if any(path.is_symlink() for path in source.rglob("*")):
            parser.error(f"Refusing to install a skill containing symlinks: {name}")
        plan.append((name, source, target))

    for name, source, target in plan:
        if entries[name]["platform"] == "windows" and sys.platform != "win32":
            print(f"NOTE: {name} requires Windows, Origin and PowerPoint to run.")
        print(f"{'PLAN' if args.dry_run else 'INSTALL' if profile['mode'] == 'local' else 'EXPORT'} [{args.agent}] {name} -> {target}")
    if args.dry_run:
        return 0

    destination.mkdir(parents=True, exist_ok=True)
    for name, source, target in plan:
        try:
            copy_skill(source, target, profile, entries[name])
        except OSError as error:
            print(f"Installation failed for {name}: {error}. Inspect the partial destination before retrying.", file=sys.stderr)
            return 1
    print('Skill files are ready. Prepare runtime software separately; see docs/SOFTWARE.md.')
    if profile['mode'] == 'chat':
        print('Chat-guidance edition: native Skill installation and local app execution are not implied.')
    if profile['mode'] == 'import':
        print('Import each skill ZIP through the host interface; use scripts/build_editions.py --agent workbuddy.')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
