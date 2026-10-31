#!/usr/bin/env python3
"""Agent-neutral local Origin, GraphPad Prism and Zotero entry points."""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2), flush=True)


def executable(app, explicit=None):
    names = {'origin': ['Origin64.exe', 'Origin.exe'], 'prism': ['prism.exe'], 'zotero': ['zotero.exe', 'zotero']}[app]
    supplied = explicit or os.environ.get(app.upper() + '_EXE')
    if supplied:
        path = Path(supplied).expanduser().resolve()
        if not path.is_file():
            raise ValueError(f'{app.upper()}_EXE is not a file')
        return path
    for name in names:
        found = shutil.which(name)
        if found:
            return Path(found)
    if sys.platform == 'win32':
        import winreg
        for hive in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
            for name in names:
                try:
                    with winreg.OpenKey(hive, 'Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\' + name) as key:
                        value = winreg.QueryValueEx(key, None)[0]
                    path = Path(value.strip('"'))
                    if path.is_file():
                        return path
                except OSError:
                    pass
        roots = [Path(value) for key in ['ProgramFiles', 'ProgramFiles(x86)', 'LOCALAPPDATA'] if (value := os.environ.get(key))]
        patterns = {'origin': ['OriginLab/Origin*/Origin64.exe'], 'prism': ['GraphPad/Prism*/prism.exe', 'GraphPad Software/Prism*/prism.exe'], 'zotero': ['Zotero/zotero.exe', 'Programs/Zotero/zotero.exe']}[app]
        for root in roots:
            for pattern in patterns:
                for path in sorted(root.glob(pattern), reverse=True):
                    if path.is_file():
                        return path
    return None


def zotero_get(path, port=23119):
    if not 1 <= port <= 65535 or not path.startswith('/'):
        raise ValueError('Invalid local API path or port')
    request = urllib.request.Request(
        f'http://127.0.0.1:{port}/api' + path,
        headers={'Zotero-API-Version': '3', 'User-Agent': 'research-app-bridge'},
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(request, timeout=10) as response:
        return response.read(), dict(response.headers)


def snapshot_outputs(paths):
    result = {}
    for value in paths:
        path = Path(value).expanduser().resolve()
        stat = path.stat() if path.is_file() else None
        result[str(path)] = (stat.st_mtime_ns, stat.st_size) if stat else None
    return result


def fresh_outputs(paths, started, baseline=None):
    records = []
    for value in paths:
        path = Path(value).expanduser().resolve()
        present = path.is_file()
        stat = path.stat() if present else None
        changed = baseline is None or baseline.get(str(path)) != ((stat.st_mtime_ns, stat.st_size) if stat else None)
        records.append({'path': str(path), 'bytes': stat.st_size if stat else 0, 'fresh': bool(stat and stat.st_size and stat.st_mtime >= started - 1 and changed)})
    return records


def wait_outputs(paths, started, timeout, baseline=None):
    deadline = time.monotonic() + timeout
    while True:
        outputs = fresh_outputs(paths, started, baseline)
        if all(row['fresh'] for row in outputs):
            return outputs
        if time.monotonic() >= deadline:
            raise TimeoutError('Expected output was not created or refreshed: ' + ', '.join(str(p) for p in paths))
        time.sleep(0.5)


def quote_prism(path):
    text = str(path)
    if any(char in text for char in ['"', '\n', '\r']):
        raise ValueError('Prism paths cannot contain quotes or newlines')
    return '"' + text + '"'


def prepare_prism(project, out_dir, graph):
    project = Path(project).expanduser().resolve()
    out_dir = Path(out_dir).expanduser().resolve()
    if not project.is_file() or project.suffix.lower() not in {'.prism', '.pzf', '.pzfx', '.pzt'}:
        raise ValueError('Supply an existing Prism project or template')
    if graph < 1:
        raise ValueError('Prism graph numbers begin at 1')
    if out_dir.exists() and any(out_dir.iterdir()):
        raise FileExistsError('Use an empty task output directory; existing contents were not changed')
    out_dir.mkdir(parents=True, exist_ok=True)
    copied = out_dir / ('source' + project.suffix)
    shutil.copy2(project, copied)
    script = out_dir / 'export.pzc'
    pdf = out_dir / 'graph.pdf'
    png = out_dir / 'graph.png'
    done = out_dir / 'done.txt'
    lines = [
        'SetPath ' + quote_prism(out_dir),
        'Open ' + quote_prism(copied),
        f'GoTo G, {graph}',
        'ExportPDF ' + quote_prism(pdf),
        'ExportPNG ' + quote_prism(png) + ' 300',
        'OpenOutput ' + quote_prism(done),
        'WText "done"',
        'CloseOutput',
    ]
    script.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\r\n')
    return {'status': 'prepared', 'script': str(script), 'project_copy': str(copied), 'expected': [str(pdf), str(png), str(done)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='app', required=True)
    doctor = commands.add_parser('doctor', help='Inspect dependencies without opening Origin or Prism')
    doctor.add_argument('--port', type=int, default=23119)
    origin = commands.add_parser('origin').add_subparsers(dest='action', required=True)
    origin_run = origin.add_parser('run')
    origin_run.add_argument('--script', type=Path, required=True)
    origin_run.add_argument('--expect', action='append', default=[])
    origin_run.add_argument('--timeout', type=float, default=300)
    prism = commands.add_parser('prism').add_subparsers(dest='action', required=True)
    prepare = prism.add_parser('prepare-export')
    prepare.add_argument('--project', type=Path, required=True)
    prepare.add_argument('--out-dir', type=Path, required=True)
    prepare.add_argument('--graph', type=int, default=1)
    run = prism.add_parser('run')
    run.add_argument('--script', type=Path, required=True)
    run.add_argument('--exe', type=Path)
    run.add_argument('--expect', action='append', default=[])
    run.add_argument('--timeout', type=float, default=120)
    zotero = commands.add_parser('zotero').add_subparsers(dest='action', required=True)
    ping = zotero.add_parser('ping')
    search = zotero.add_parser('search')
    search.add_argument('--query', required=True)
    search.add_argument('--limit', type=int, default=10)
    item = zotero.add_parser('item')
    item.add_argument('--key', required=True)
    export = zotero.add_parser('export')
    export.add_argument('--keys', nargs='+', required=True)
    export.add_argument('--format', choices=['ris', 'bibtex'], default='ris')
    export.add_argument('--out', type=Path, required=True)
    for subparser in [ping, search, item, export]:
        subparser.add_argument('--port', type=int, default=23119)
    args = parser.parse_args()

    if args.app == 'doctor':
        report = {'python': sys.version.split()[0], 'executable': sys.executable, 'platform': platform.system(), 'applications': {}, 'originpro_available': importlib.util.find_spec('originpro') is not None}
        for app in ['origin', 'prism', 'zotero']:
            path = executable(app)
            report['applications'][app] = str(path) if path else None
        try:
            _, headers = zotero_get('/', args.port)
            report['zotero_api'] = {'reachable': True, 'api_version': headers.get('Zotero-API-Version', '3')}
        except (OSError, urllib.error.URLError) as error:
            report['zotero_api'] = {'reachable': False, 'reason': str(error)}
        emit(report)
    elif args.app == 'origin':
        if sys.platform != 'win32':
            raise RuntimeError('Origin automation requires native Windows, not a Linux/WSL or cloud interpreter')
        if importlib.util.find_spec('originpro') is None:
            raise RuntimeError('Install originpro in this Python environment; see references/software.md')
        script = args.script.expanduser().resolve()
        if not script.is_file() or script.suffix.lower() != '.py':
            raise ValueError('Provide an existing task-specific Python script')
        baseline = snapshot_outputs(args.expect)
        started = time.time()
        result = subprocess.run([sys.executable, str(script)], cwd=script.parent, timeout=args.timeout)
        if result.returncode:
            raise RuntimeError(f'Origin task script exited with {result.returncode}')
        outputs = wait_outputs(args.expect, started, 1, baseline) if args.expect else []
        emit({'status': 'script_completed', 'outputs': outputs, 'visual_review': 'not_performed_by_bridge'})
    elif args.app == 'prism' and args.action == 'prepare-export':
        emit(prepare_prism(args.project, args.out_dir, args.graph))
    elif args.app == 'prism':
        if sys.platform != 'win32':
            raise RuntimeError('This launcher supports native Windows; see references/prism.md for the macOS route')
        path = executable('prism', args.exe)
        if not path:
            raise RuntimeError('Prism executable was not found; set PRISM_EXE or pass --exe')
        script = args.script.expanduser().resolve()
        if not script.is_file() or script.suffix.lower() != '.pzc':
            raise ValueError('Provide an existing .pzc script')
        baseline = snapshot_outputs(args.expect)
        started = time.time()
        process = subprocess.Popen([str(path), '@' + str(script)], cwd=script.parent)
        outputs = wait_outputs(args.expect, started, args.timeout, baseline) if args.expect else []
        emit({'status': 'outputs_created' if outputs else 'dispatched', 'pid': process.pid, 'outputs': outputs, 'visual_review': 'not_performed_by_bridge'})
    else:
        if args.action == 'ping':
            _, headers = zotero_get('/', args.port)
            emit({'status': 'reachable', 'api_version': headers.get('Zotero-API-Version', '3')})
        elif args.action == 'search':
            if not 1 <= args.limit <= 100:
                raise ValueError('Use a search limit between 1 and 100')
            query = urllib.parse.urlencode({'q': args.query, 'limit': args.limit, 'format': 'json', 'itemType': '-attachment'})
            data, _ = zotero_get('/users/0/items/top?' + query, args.port)
            rows = json.loads(data)
            emit({'items': [{'key': row['key'], 'data': row['data']} for row in rows]})
        elif args.action == 'item':
            if not re.fullmatch('[A-Z0-9]{8}', args.key):
                raise ValueError('Zotero item keys have eight uppercase letters or digits')
            data, _ = zotero_get('/users/0/items/' + args.key, args.port)
            emit(json.loads(data))
        else:
            if any(not re.fullmatch('[A-Z0-9]{8}', key) for key in args.keys):
                raise ValueError('Invalid Zotero item key')
            output = args.out.expanduser().resolve()
            if output.exists():
                raise FileExistsError('Export target already exists; choose a new file name')
            query = urllib.parse.urlencode({'itemKey': ','.join(dict.fromkeys(args.keys)), 'format': args.format})
            data, _ = zotero_get('/users/0/items?' + query, args.port)
            if not data.strip():
                raise RuntimeError('Zotero returned an empty export')
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(data)
            emit({'status': 'exported', 'path': str(output), 'bytes': len(data), 'library_modified': False})
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as error:
        emit({'status': 'error', 'type': type(error).__name__, 'message': str(error)})
        raise SystemExit(2)
