#!/usr/bin/env python3
"""Copy selected skills to a host skill directory without replacing existing data."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    catalog = json.loads((root / "skills.json").read_text(encoding="utf-8"))
    entries = {entry["name"]: entry for entry in catalog["skills"]}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill", action="append", choices=sorted(entries), help="Repeat to select multiple skills")
    parser.add_argument("--dest", type=Path, help="Host skill directory; defaults to CODEX_HOME/skills or ~/.codex/skills")
    parser.add_argument("--dry-run", action="store_true", help="Show the plan without writing files")
    args = parser.parse_args()
    if not args.skill:
        parser.print_help()
        return 0

    codex_base = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    destination = (args.dest or codex_base / "skills").expanduser().resolve()
    plan = []
    for name in dict.fromkeys(args.skill):
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
        print(f"{'PLAN' if args.dry_run else 'INSTALL'} {name} -> {target}")
    if args.dry_run:
        return 0

    destination.mkdir(parents=True, exist_ok=True)
    for name, source, target in plan:
        try:
            shutil.copytree(source, target, ignore=shutil.ignore_patterns(
                "__pycache__", "*.pyc", ".venv", ".git", ".env", "config.yaml", "auth.json"
            ))
        except OSError as error:
            print(f"Installation failed for {name}: {error}. Inspect the partial destination before retrying.", file=sys.stderr)
            return 1
    print("Installed skill files. Prepare the selected skill's runtime separately, then reload your host's skill list.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
