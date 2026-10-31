#!/usr/bin/env python3
"""Build self-contained agent ZIPs and WorkBuddy single-skill import packages."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
from edition_tools import ROOT, adapt_skill, include_file, profiles


def main():
    hosts = profiles()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', action='append', choices=hosts)
    parser.add_argument('--out', type=Path, default=ROOT / 'dist')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'skills.json').read_text(encoding='utf-8'))
    entries = {row['path'] + '/SKILL.md': row for row in catalog['skills']}
    output = args.out.expanduser().resolve()
    if output == ROOT or ROOT.is_relative_to(output):
        parser.error('Output must not be the source repository or its ancestor')
    files = [path for path in ROOT.rglob('*') if path.is_file() and include_file(path.relative_to(ROOT)) and not path.is_relative_to(output)]
    output.mkdir(parents=True, exist_ok=True)
    checksums = []
    for agent in args.agent or hosts:
        profile = hosts[agent]
        archive = output / f'research-ppt-skills-{agent}-v{catalog["version"]}.zip'
        prefix = f'research-ppt-skills-{agent}/'
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as package:
            for path in files:
                relative = path.relative_to(ROOT).as_posix()
                if relative in {'edition.json', 'EDITION.md'}:
                    continue
                if agent != 'codex' and relative.startswith('skills/') and relative.endswith('/agents/openai.yaml'):
                    continue
                data = path.read_bytes()
                if relative in entries:
                    data = adapt_skill(data.decode('utf-8-sig'), profile, entries[relative]).encode('utf-8')
                package.writestr(prefix + relative, data)
            package.writestr(prefix + 'edition.json', json.dumps({'agent': agent, 'version': catalog['version']}, indent=2))
            package.writestr(prefix + 'EDITION.md', (ROOT / 'editions' / agent / 'README.md').read_bytes())
        checksums.append((archive.name, hashlib.sha256(archive.read_bytes()).hexdigest()))
        print(archive)
        if agent == 'workbuddy':
            target_dir = output / 'workbuddy'
            target_dir.mkdir(exist_ok=True)
            for entry in catalog['skills']:
                source = ROOT / entry['path']
                target = target_dir / f'{entry["name"]}-workbuddy-v{catalog["version"]}.zip'
                with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as package:
                    for path in source.rglob('*'):
                        relative = path.relative_to(source)
                        if not path.is_file() or not include_file(relative) or relative.as_posix() == 'agents/openai.yaml':
                            continue
                        data = path.read_bytes()
                        if relative.as_posix() == 'SKILL.md':
                            data = adapt_skill(data.decode('utf-8-sig'), profile, entry).encode('utf-8')
                        package.writestr(entry['name'] + '/' + relative.as_posix(), data)
                checksums.append(('workbuddy/' + target.name, hashlib.sha256(target.read_bytes()).hexdigest()))
                print(target)
    (output / 'SHA256SUMS.txt').write_text('\n'.join(value + '  ' + name for name, value in checksums) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
