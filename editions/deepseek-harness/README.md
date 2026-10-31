# DeepSeek Harness 版

按官方项目安装 Node.js 后，可使用：

```bash
npx @deepseek-ai/dsh web
python scripts/install_skills.py --agent deepseek-harness --all
```

安装器默认使用 `$DSH_HOME/skills`，未设置时为 `~/.dsh/skills`；项目级使用 `--project <项目目录>`。Harness 必须加载本地 skill provider 以及任务所需的文件/命令执行插件。

官方：[项目与运行说明](https://github.com/deepseek-ai/deepseek-harness)、[技能目录与配置](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md)。该项目仍在快速迭代，以所装版本的实际插件能力为准。
