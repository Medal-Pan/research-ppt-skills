# Codex 版

适合使用 Codex 本地文件、终端和图片工具的用户。安装：

```bash
python scripts/install_skills.py --agent codex --all --dry-run
python scripts/install_skills.py --agent codex --all
```

默认使用 `~/.agents/skills`；需要兼容当前旧安装时用 `--dest` 指定已有宿主目录。已有同名技能不覆盖。官方：[技能发现与调用](https://learn.chatgpt.com/docs/build-skills)。
