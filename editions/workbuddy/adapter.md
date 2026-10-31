# WorkBuddy 适配

本版按 WorkBuddy 官方技能结构补入展示名称、双语描述、版本与作者字段。导入时使用单个技能 ZIP，保留其 `scripts/` 与 `references/`；不要只粘贴一个 `SKILL.md` 后期待脚本自动存在。

使用 WorkBuddy 实际提供的 Bash/终端和文件工具调用本地 Python。若技能执行于远端环境，须先确认能否访问用户电脑；不能把安装了 WorkBuddy 等同于已接通 Origin、Prism 或 Zotero。

图片生成使用当前宿主能力或用户配置的兼容服务，不使用 Codex OAuth。软件协作通过 `research-app-bridge` 的命令入口完成；缺少执行权限或软件时，报告具体缺项和已产生的文件。
