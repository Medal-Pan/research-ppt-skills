"""Distribution and protocol checks; never launches commercial desktop apps."""
from __future__ import annotations
from contextlib import contextmanager, redirect_stdout
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import uuid
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from edition_tools import adapt_skill, profiles

spec = importlib.util.spec_from_file_location('research_bridge', ROOT / 'skills/research-app-bridge/scripts/app_bridge.py')
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


@contextmanager
def scratch():
    parent = (ROOT / 'dist/test-runs').resolve()
    if not parent.is_relative_to(ROOT):
        raise RuntimeError('Test temporary root escapes repository')
    parent.mkdir(parents=True, exist_ok=True)
    target = parent / ('case-' + uuid.uuid4().hex)
    target.mkdir()
    try:
        yield str(target)
    finally:
        resolved = target.resolve()
        if target.is_symlink() or not resolved.is_relative_to(parent) or not target.name.startswith('case-'):
            raise RuntimeError('Test cleanup target escapes its owner')
        shutil.rmtree(resolved)


def metadata(text):
    return yaml.safe_load(re.match(r'---\n(.*?)\n---', text, re.S).group(1))


class EditionsTest(unittest.TestCase):
    def test_all_agent_installs_and_retargeting(self):
        catalog = json.loads((ROOT / 'skills.json').read_text(encoding='utf-8'))
        with scratch() as temp:
            for agent in profiles():
                destination = Path(temp) / agent
                result = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT/'scripts/install_skills.py'), '--agent', agent, '--all', '--dest', str(destination)], capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(result.returncode, 0, result.stderr)
                for entry in catalog['skills']:
                    folder = destination / entry['name']
                    text = (folder/'SKILL.md').read_text(encoding='utf-8')
                    data = metadata(text)
                    self.assertEqual(data['name'], entry['name'])
                    self.assertEqual(text.count('<!-- agent-edition:start -->'), 1)
                    self.assertTrue((folder/'LICENSE').is_file())
                    if agent == 'workbuddy':
                        for field in ['display_name','display_name_en','description_zh','description_en','version','author']:
                            self.assertTrue(data.get(field), field)
                    if agent != 'codex':
                        self.assertFalse((folder/'agents/openai.yaml').exists())
            source = (ROOT/'skills/nature-paper2ppt/SKILL.md').read_text(encoding='utf-8')
            entry = next(row for row in catalog['skills'] if row['name']=='nature-paper2ppt')
            transformed = adapt_skill(adapt_skill(source, profiles()['workbuddy'], entry), profiles()['claude-code'], entry)
            self.assertNotIn('display_name', metadata(transformed))
            self.assertEqual(transformed.count('<!-- agent-edition:start -->'), 1)
            self.assertIn('Claude Code 适配', transformed)
            self.assertNotIn('# WorkBuddy 适配', transformed)

    def test_no_overwrite_and_preflight(self):
        with scratch() as temp:
            command = [sys.executable, '-X', 'utf8', str(ROOT/'scripts/install_skills.py'), '--agent', 'claude-code', '--dest', temp]
            first = subprocess.run(command + ['--skill','image-to-editable-ppt'], capture_output=True)
            self.assertEqual(first.returncode, 0)
            path = Path(temp)/'image-to-editable-ppt/SKILL.md'
            before = hashlib.sha256(path.read_bytes()).hexdigest()
            second = subprocess.run(command + ['--skill','nature-paper2ppt','--skill','image-to-editable-ppt'], capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertFalse((Path(temp)/'nature-paper2ppt').exists())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), before)

    def test_complete_archives_and_workbuddy_imports(self):
        with scratch() as temp:
            result = subprocess.run([sys.executable, '-X','utf8',str(ROOT/'scripts/build_editions.py'),'--out',temp],capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
            self.assertEqual(len(list(Path(temp).glob('*.zip'))), 5)
            self.assertEqual(len(list((Path(temp)/'workbuddy').glob('*.zip'))), 6)
            for archive in Path(temp).rglob('*.zip'):
                with zipfile.ZipFile(archive) as package:
                    self.assertIsNone(package.testzip())
                    names = package.namelist()
                    self.assertFalse(any('/.git/' in name or name.endswith('/config.yaml') or name.endswith('/.env') for name in names))
                    if archive.parent.name == 'workbuddy':
                        skills = [name for name in names if name.endswith('/SKILL.md')]
                        self.assertEqual(len(skills), 1)
                        self.assertTrue(metadata(package.read(skills[0]).decode())['display_name'])


class BridgeTest(unittest.TestCase):
    def test_prism_copy_and_script(self):
        with scratch() as temp:
            source = Path(temp)/'input.pzfx'
            source.write_text('<GraphPadPrismFile/>')
            before = source.read_bytes()
            report = bridge.prepare_prism(source, Path(temp)/'work', 2)
            text = Path(report['script']).read_text(encoding='utf-8')
            self.assertIn('GoTo G, 2', text)
            self.assertIn('ExportPDF ', text)
            self.assertIn('ExportPNG ', text)
            self.assertIn('CloseOutput', text)
            self.assertEqual(source.read_bytes(), before)
            with self.assertRaises(FileExistsError):
                bridge.prepare_prism(source, Path(temp)/'work', 2)

    def test_prism_official_launch_argument(self):
        with scratch() as temp:
            script = Path(temp)/'export.pzc'
            script.write_text('GoTo G, 1\n')
            with patch.object(bridge.sys, 'platform', 'win32'), patch.object(bridge, 'executable', return_value=Path('Prism.exe')), patch.object(bridge.subprocess, 'Popen') as launched, patch.object(sys, 'argv', ['app_bridge.py','prism','run','--script',str(script)]), redirect_stdout(io.StringIO()) as output:
                launched.return_value.pid = 123
                self.assertEqual(bridge.main(), 0)
                self.assertEqual(launched.call_args.args[0][1], '@' + str(script.resolve()))
                self.assertEqual(json.loads(output.getvalue())['status'], 'dispatched')

    def test_stale_file_is_not_a_completed_output(self):
        with scratch() as temp:
            path = Path(temp)/'old.png'
            path.write_bytes(b'old')
            baseline = bridge.snapshot_outputs([path])
            self.assertFalse(bridge.fresh_outputs([path], time.time(), baseline)[0]['fresh'])
            path.write_bytes(b'new-and-changed')
            self.assertTrue(bridge.fresh_outputs([path], time.time(), baseline)[0]['fresh'])

    def test_zotero_local_read_protocol(self):
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                requests.append(self.path)
                parsed = urlsplit(self.path)
                query = parse_qs(parsed.query)
                if parsed.path == '/api/':
                    body = b'{}'
                elif query.get('format') == ['ris']:
                    body = b'TY  - JOUR\nTI  - Test fixture\nER  -\n'
                else:
                    body = json.dumps([{'key':'ABCD1234','data':{'title':'Test fixture'}}]).encode()
                self.send_response(200)
                self.send_header('Zotero-API-Version','3')
                self.end_headers()
                self.wfile.write(body)
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1',0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            port = str(server.server_address[1])
            with patch.object(sys,'argv',['app_bridge.py','zotero','search','--query','test','--limit','3','--port',port]), redirect_stdout(io.StringIO()) as output:
                bridge.main()
                self.assertEqual(json.loads(output.getvalue())['items'][0]['key'],'ABCD1234')
            with scratch() as temp:
                target = Path(temp)/'selected.ris'
                args = ['app_bridge.py','zotero','export','--keys','ABCD1234','--out',str(target),'--port',port]
                with patch.object(sys,'argv',args), redirect_stdout(io.StringIO()):
                    bridge.main()
                self.assertIn('Test fixture', target.read_text())
                with patch.object(sys,'argv',args), self.assertRaises(FileExistsError):
                    bridge.main()
            self.assertEqual(parse_qs(urlsplit(requests[-1]).query)['itemKey'],['ABCD1234'])
            self.assertTrue(all(path.startswith('/api/users/0/') for path in requests))
        finally:
            server.shutdown()
            server.server_close()


if __name__ == '__main__':
    unittest.main()
