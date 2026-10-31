---
name: research-app-bridge
description: "让不同 Agent 通过统一 Python 命令协作调用本机 Origin、GraphPad Prism 和 Zotero：检查环境、执行 Origin 脚本、生成和运行 Prism 导出脚本、检索 Zotero 与导出参考文献。用于科研软件协作、跨 Agent 自动化和文献到科研图组工作流。"
---

# 科研软件协作

本技能不依赖 Codex 专有工具。将 `<SKILL>` 替换为本文件所在目录，用宿主实际提供的终端/执行命令工具调用 `scripts/app_bridge.py`。若只有聊天能力，则提供命令让用户在本机运行，并根据返回的 JSON 继续；不能声称已执行本机操作。

## 先检查环境

读 [软件安装与下载](references/software.md)，然后运行：

```bash
python <SKILL>/scripts/app_bridge.py doctor
```

`doctor` 检测路径、Python 模块和 Zotero 接口，不启动 Origin/Prism，也不等同于完整自动化验证。缺项按报告解决；使用 Origin/Prism 前还要确认本机有效许可。不要通过修改全局配置或安装包来绕过许可。

## 按任务调用

- **Origin / OriginPro**：读 [Origin 工作流](references/origin.md)。在原生 Windows Python 中执行任务脚本；保留真实数据、样式契约、`.opju`、预览与检查结果。用自身脚本的输出确认 COM 已连接，不能把检测到安装路径当成执行成功。
- **GraphPad Prism**：读 [Prism 工作流](references/prism.md)。优先复用用户已有项目/分析模板，复制到任务目录后再操作；通过官方 `.pzc` 脚本接口调用。后台启动状态为 `dispatched`，只有实际导出文件生成后才能报告完成。不得凭空给出统计结果。
- **Zotero**：读 [Zotero 工作流](references/zotero.md)。本地 API 默认只读，先检索并核对条目，再按条目 key 导出 RIS/BibTeX。不得读取 SQLite 数据库、扫描全库附件或猜测引用元数据。

## 快捷命令

```bash
python <SKILL>/scripts/app_bridge.py origin run --script ./task/build_origin.py --expect ./task/figure.opju
python <SKILL>/scripts/app_bridge.py prism prepare-export --project ./input/source.pzfx --out-dir ./task/prism --graph 1
python <SKILL>/scripts/app_bridge.py prism run --script ./task/prism/export.pzc --expect ./task/prism/graph.pdf
python <SKILL>/scripts/app_bridge.py zotero search --query "food protein" --limit 10
python <SKILL>/scripts/app_bridge.py zotero export --keys ABCD1234 EFGH5678 --format ris --out ./task/references.ris
```

所有路径由当前任务提供。未识别软件位置时用 `ORIGIN_EXE`、`PRISM_EXE` 或 `ZOTERO_EXE` 指向本机安装文件；这些本机路径不要写入公开仓库。Origin 的脚本运行另需当前解释器安装 `originpro`。

## 交付与边界

报告调用命令、解释器、实际输出路径、文件存在/大小和残留问题。查看图像预览后再给出视觉结论。应用启动、命令返回 0、生成文件和通过内容检查是不同证据。不得把静态截图称为可编辑项目，也不得将聊天端的命令建议称为实际软件操作。
