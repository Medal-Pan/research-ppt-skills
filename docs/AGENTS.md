# 选择 Agent 版本

这些版本共享同一套核心技能，区别在安装结构、宿主指令、生图路线和执行能力。打包/安装检查通过不等于在每个 Agent 中完成端到端制作实测。

| 版本 | 使用方式 | 本机软件协作 |
| --- | --- | --- |
| [Codex](../editions/codex/README.md) | 当前官方用户目录 `~/.agents/skills`；可指定旧目录 | 本地执行环境具备权限时可用 |
| [Claude Code](../editions/claude-code/README.md) | `~/.claude/skills` 或项目 `.claude/skills` | 原生 Windows 可调用本机软件；云端/WSL 另行安排 |
| [DeepSeek Harness](../editions/deepseek-harness/README.md) | `$DSH_HOME/skills` / `~/.dsh/skills`，项目 `.dsh/skills` | 取决于 Harness 所在主机与已启用插件 |
| [WorkBuddy](../editions/workbuddy/README.md) | 单技能 ZIP 导入；补齐官方展示字段 | 取决于本地终端/桌面权限；不假定内部目录 |
| [豆包](../editions/doubao/README.md) | 对话引导材料与本机命令配套 | 没有本机执行接口时由用户执行命令后回传结果 |

不同宿主不能共享 Codex OAuth。其他 Agent 的生图使用自己实际提供的能力，或独立配置的兼容 API；未配置时不伪装成本地绘图替代生成。

## 安装与导出

```bash
python scripts/install_skills.py --agent claude-code --all --dry-run
python scripts/install_skills.py --agent claude-code --all
python scripts/install_skills.py --agent deepseek-harness --all --project ./my-project
python scripts/install_skills.py --agent workbuddy --all --dest ./workbuddy-import
python scripts/install_skills.py --agent doubao --all --dest ./doubao-guide
```

若只需要一个技能，用 `--skill <名称>` 替代 `--all`。已有同名目录时停止，不覆盖本机个性化修改。Codex 老版本/自定义目录可用 `--dest` 显式指定。

生成五个独立版本的完整 ZIP，以及 WorkBuddy 所需的单技能 ZIP：

```bash
python scripts/build_editions.py
```

产物位于 `dist/`，包含 SHA256 校验清单。每个完整 ZIP 带有 `edition.json` 与对应 `EDITION.md`，安装器会默认选择该版本；解压后仍可显式指定另一个 `--agent`。

## 如何确认是真的可用

1. 在宿主技能列表中找到技能，或按其官方方式显式加载。
2. 验证能读取一个测试文件并在任务输出目录写文件。
3. 运行软件桥 `doctor`，检查执行主机、解释器和应用/接口。
4. 使用自己的最小任务运行目标软件，核对实际输出和预览。

没有本机执行能力的聊天端，最多完成它能运行的内容与脚本准备；不要把指令文本、进程启动或假想效果写成已完成的工程。

官方依据：[Codex](https://learn.chatgpt.com/docs/build-skills)、[Claude Code](https://code.claude.com/docs/en/skills)、[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md)、[WorkBuddy](https://open.workbuddy.cn/docs/skill)。豆包部分是本项目提供的对话适配策略，未宣称存在通用原生 Skill 安装协议。
