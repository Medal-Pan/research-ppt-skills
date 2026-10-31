# Claude Code 版

适合 Claude Code 的本地 CLI/桌面代码任务。安装：

```bash
python scripts/install_skills.py --agent claude-code --all
```

默认复制到 `~/.claude/skills`；项目级可使用 `--project <项目目录>`。调用示例：`/nature-paper2ppt`。原生 Windows 才能直接调用 Origin/本项目 Prism 启动器。

官方下载与安装：[Claude Code setup](https://code.claude.com/docs/en/setup)。Windows 可用官方 `winget install Anthropic.ClaudeCode`；macOS/Linux 按官网命令安装。普通 Claude 网页对话不等同于本地 Claude Code，云端执行不能直接访问用户电脑应用。
