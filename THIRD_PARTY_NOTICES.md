# 来源、许可与发布范围

本合集由 Medal-Pan 整理。保留本地使用版本的工作流规则；第三方内容的作者身份和许可不随整理而改变。

| 路径 | 来源 | 许可 | 发布处理 |
| --- | --- | --- | --- |
| `skills/image-to-editable-ppt` | 本次对话中按用户提供的混合重建要求整理 | MIT | 新编技能，包含调用入口 |
| `skills/research-app-bridge` | 本合集新增，接口与命令依据原厂公开文档 | MIT | Agent 中立的本机应用调用入口与工作流；不包含商业软件本体 |
| `skills/nature-paper2ppt` | [Paul-Jeo/nature-skills](https://github.com/Paul-Jeo/nature-skills/tree/main/skills/nature-paper2ppt) | Apache-2.0 | 使用本地版本，补入上游根许可证；共享术语文件打包到技能内部，改动文件已注明 |
| `skills/nature-paper2ppt/references/terminology-ledger.md` | [nature-shared](https://github.com/Paul-Jeo/nature-skills/blob/main/skills/nature-shared/core/terminology-ledger.md) | Apache-2.0 | 随论文汇报技能分发，消除跨技能目录依赖 |
| `skills/nature-image2ppt` | [Paul-Jeo/Image2PPT](https://github.com/Paul-Jeo/Image2PPT)，来源提交 `3bcedf41a277a3a4ae8024f6030437930c969d30`，见原 `manifest.yaml` | MIT | 保留原许可证及 Image2PPT contributors、ningzimu 署名，不改运行时 |
| `skills/codex-ppt` | [ningzimu/codex-ppt-skill](https://github.com/ningzimu/codex-ppt-skill) | MIT | 使用本地版本，补入上游许可证；不带个人配置和 API 凭据 |
| `skills/ace-sci-origin` | [hzsci/ace-sci-origin](https://github.com/hzsci/ace-sci-origin) | MIT | 保留“研理科研线”的作者与许可证 |

没有保留版本号或源提交的本地版本不标称为上游最新版。每个技能目录中的 `LICENSE` 优先约束该目录内容。

## 仅链接的本机配套工具

- [PPT Master](https://github.com/hugohe3/ppt-master)：作者 Hugo He，MIT。完整工具、图标库及署名由原仓库提供，本合集不复制其大体积运行资源。
- [Vivid Illustration Skill](https://github.com/yjz211/vivid-illustration-skill)：许可限制修改、衍生及再分发，仅链接到原仓库。
- 本机 `presentations` 为宿主提供的能力，本合集不复制其专属运行库。

## 文档组织参考

参考以下项目展示用途、安装、使用示例、目录与能力边界的组织方式。本仓库的介绍与示例重新撰写，未复制其演示图、赞助信息或效果声明。

- [paper2ppt-skill](https://github.com/ablikimeli/paper2ppt-skill)：输入类型、功能与调用示例。
- [paper2slides-skill](https://github.com/inhyeoklee/paper2slides-skill)：工作流与交付物说明。
- [PPT Master](https://github.com/hugohe3/ppt-master)：能力边界与文档导航。

## 本次发布改动

- 在独立发布目录复制选定技能，原安装目录保持原样。
- 将论文汇报技能的共享术语依赖收进自身 `references/`，并更新两处路径；标注改动。
- 为单独分发的目录补齐相应许可证、来源与必要依赖说明。
- 新增合集文档、选择性安装工具和结构检查；没有改写第三方运行时算法。
- 排除配置、凭据、缓存、本机实验文件及生成的 PPT/PDF/Origin 工程。

## 0.2.0 更新

- 添加按 Codex、Claude Code、DeepSeek Harness、WorkBuddy 和豆包对话引导版生成的适配包；非 Codex 版本不假定可用 Codex OAuth 或专属工具。
- 给五个演示技能补充软件要求引用，改动文件保留分发更新说明；原许可证继续保留。
- 新增科研软件命令桥与原厂下载指南；Zotero 入口只读，不直接修改资料库。
- 工作方式图改为文字优先的浅色流程图，使用内置 imagegen 生成/编辑；没有复用第三方演示图片。
