#!/usr/bin/env python3
"""Validate distribution structure and portability; does not run PPT generation."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

import yaml


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures: list[str] = []
    catalog = json.loads((root / "skills.json").read_text(encoding="utf-8"))
    entries = catalog["skills"]
    names = [entry["name"] for entry in entries]
    if len(set(names)) != len(names):
        failures.append("Duplicate catalog names")
    for entry in entries:
        folder = (root / entry["path"]).resolve()
        if not folder.is_relative_to(root / "skills"):
            failures.append(f"Skill path escapes skills/: {entry['name']}")
            continue
        skill = folder / "SKILL.md"
        if not skill.is_file() or not (folder / "LICENSE").is_file():
            failures.append(f"Missing SKILL.md or LICENSE: {entry['name']}")
            continue
        text = skill.read_text(encoding="utf-8-sig")
        front = re.match(r"\A---\r?\n(.*?)\r?\n---", text, re.S)
        if not front:
            failures.append(f"Invalid frontmatter: {entry['name']}")
            continue
        metadata = yaml.safe_load(front.group(1))
        if metadata.get("name") != entry["name"] or not metadata.get("description"):
            failures.append(f"Invalid name or description: {entry['name']}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", entry["name"]):
            failures.append(f"Invalid skill name: {entry['name']}")

    paper = root / "skills/nature-paper2ppt"
    manifest = yaml.safe_load((paper / "manifest.yaml").read_text(encoding="utf-8"))
    references = list(manifest["always_load"])
    references.extend(manifest["axes"]["paper_type"]["values"].values())
    references.extend(item["path"] for item in manifest["references"]["on_demand"])
    references.append(manifest["quality_tools"]["pptx_audit_script"])
    for relative in references:
        target = (paper / relative).resolve()
        if not target.is_relative_to(paper) or not target.is_file():
            failures.append(f"Paper skill dependency is missing or external: {relative}")

    image_root = root / "skills/nature-image2ppt"
    runtime = yaml.safe_load((image_root / "manifest.yaml").read_text(encoding="utf-8"))["runtime"]
    for key in ("entrypoint", "requirements", "config_template"):
        target = (image_root / runtime[key]).resolve()
        if not target.is_relative_to(image_root) or not target.is_file():
            failures.append(f"Image2PPT runtime path missing or external: {key}")

    token_patterns = [
        re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
        re.compile(r"github_pat_[A-Za-z0-9_]{50,}"),
        re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{32,}"),
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    ]
    count = python_count = 0
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if any(part in {".git", "__pycache__", ".venv", ".pytest_cache"} for part in relative.parts):
            continue
        if path.is_symlink():
            failures.append(f"Symlink in distribution: {relative}")
            continue
        if not path.is_file():
            continue
        count += 1
        if path.name in {".env", "config.yaml", "auth.json", "credentials.json"} or (
            path.name.startswith(".env.") and path.name != ".env.example"
        ):
            failures.append(f"Private configuration in distribution: {relative}")
        if path.suffix.lower() in {".pptx", ".pdf", ".opju", ".pem", ".key", ".pyc"}:
            failures.append(f"Unexpected binary or private file: {relative}")
        try:
            content = path.read_text(encoding="utf-8-sig")
        except UnicodeError:
            if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
                failures.append(f"Unexpected non-UTF-8 content: {relative}")
            continue
        if any(pattern.search(content) for pattern in token_patterns):
            failures.append(f"Potential credential; inspect before publishing: {relative}")
        if re.search(r"[CD]:[\\/]Users[\\/]庆尘|D:[\\/]科研软件", content):
            failures.append(f"Personal local path: {relative}")
        if path.suffix == ".py":
            python_count += 1
            try:
                ast.parse(content, filename=str(relative))
            except SyntaxError as error:
                failures.append(f"Python syntax error in {relative}: {error.msg}")
        if path.suffix == ".json":
            try:
                json.loads(content)
            except ValueError as error:
                failures.append(f"JSON error in {relative}: {error}")
        if path.suffix == ".svg":
            try:
                ElementTree.fromstring(content)
            except ElementTree.ParseError as error:
                failures.append(f"SVG error in {relative}: {error}")
        if path.suffix == ".md":
            prose = re.sub(r"(?ms)^```[^\n]*\n.*?^```[^\n]*$", "", content)
            prose = re.sub(r"`+[^`\n]*`+", "", prose)
            for link in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", prose):
                link = link.strip("<>")
                parsed = urlsplit(link)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                target = (path.parent / unquote(parsed.path)).resolve()
                if not target.is_relative_to(root) or not target.exists():
                    failures.append(f"Broken local Markdown link in {relative}: {link}")

    if failures:
        print("\n".join(f"FAIL: {failure}" for failure in failures))
        return 1
    print(f"PASS: {len(entries)} skills, {count} files, {python_count} Python files; manifests, links and distribution checks passed.")
    print("This is a structural check, not an end-to-end PPT generation or visual quality test.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
