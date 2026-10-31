"""Shared deterministic packaging for agent editions; standard library only."""
from __future__ import annotations
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]


def profiles():
    return {row['id']: row for row in json.loads((ROOT / 'editions/profiles.json').read_text(encoding='utf-8'))['profiles']}


def include_file(relative):
    if any(part in {'.git', '.venv', 'venv', '__pycache__', '.pytest_cache', 'dist', 'agent-exports'} for part in relative.parts):
        return False
    if relative.name in {'.env', 'config.yaml', 'auth.json', 'credentials.json'}:
        return False
    if relative.name.startswith('.env.') and relative.name != '.env.example':
        return False
    return relative.suffix not in {'.pyc', '.pyo'}


def adapt_skill(text, profile, entry):
    text = text.replace('\r\n', '\n')
    text = re.sub(r'\n?# agent-edition-metadata:start\n.*?# agent-edition-metadata:end\n?', '\n', text, flags=re.S)
    text = re.sub(r'\n?<!-- agent-edition:start -->.*?<!-- agent-edition:end -->\n?', '\n', text, flags=re.S)
    match = re.match(r'\A---\n(.*?)\n---(.*)\Z', text, re.S)
    if not match:
        raise ValueError('Invalid skill frontmatter: ' + entry['name'])
    front, body = match.groups()
    if profile['id'] == 'workbuddy':
        additions = {
            'display_name': entry['title_zh'], 'display_name_en': entry['name'],
            'description_zh': entry['summary_zh'], 'description_en': entry['summary_en'],
            'version': '0.2.0', 'author': 'Medal-Pan (packaging); original authors retained in LICENSE',
        }
        front += '\n# agent-edition-metadata:start\n' + '\n'.join(key + ': ' + json.dumps(value, ensure_ascii=False) for key, value in additions.items()) + '\n# agent-edition-metadata:end'
    adapter = (ROOT / 'editions' / profile['id'] / 'adapter.md').read_text(encoding='utf-8').strip()
    section = '\n\n<!-- agent-edition:start -->\n<!-- Distribution adaptation by Medal-Pan, 2026-10-31. Upstream instructions and licenses retained. -->\n' + adapter + '\n<!-- agent-edition:end -->\n'
    return '---\n' + front.strip() + '\n---' + section + '\n' + body.lstrip('\n')


def copy_skill(source, target, profile, entry):
    if target.exists():
        raise FileExistsError(str(target))
    def ignored(folder, names):
        result = []
        for name in names:
            relative = (Path(folder) / name).relative_to(source)
            if not include_file(relative) or (profile['id'] != 'codex' and relative.as_posix() == 'agents/openai.yaml'):
                result.append(name)
        return result
    shutil.copytree(source, target, ignore=ignored)
    skill = target / 'SKILL.md'
    skill.write_text(adapt_skill(skill.read_text(encoding='utf-8-sig'), profile, entry), encoding='utf-8', newline='\n')
