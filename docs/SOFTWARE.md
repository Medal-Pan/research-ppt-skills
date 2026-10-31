# 需要安装哪些软件

核对日期：2026-10-31。按任务安装，不要求把所有软件都装一遍。下表提供原厂下载入口与安装方法；本仓库不再分发商业软件安装包、许可文件或个人 API 配置。

## 按技能准备

| 技能 / 任务 | 必需 | 按需 |
| --- | --- | --- |
| 论文汇报 `nature-paper2ppt` | 可执行文件任务的 Agent、Python、PyMuPDF/Pillow/python-pptx | PowerPoint 或 LibreOffice 渲染 |
| 轻量图片复现 `image-to-editable-ppt` | 读图及 PPTX 写出能力，通常使用 Python 与 python-pptx | 可靠渲染器；复杂图片编辑服务 |
| 精细重建 `nature-image2ppt` | 本技能 requirements、成功的 doctor 预检、渲染器 | 公式 TeX 工具、OCR/图片服务 |
| 图片式 PPT `codex-ppt` | 本技能 requirements、真实可用的生图/编辑图能力 | 所选兼容 API 的账号与本机配置 |
| Origin OLE 图组 `ace-sci-origin` | 原生 Windows、Origin/OriginPro、Microsoft PowerPoint、外部 Python | `originpro`、`pywin32`，以及数据处理包 |
| 本地软件协作 `research-app-bridge` | Python；只需安装当前使用的应用 | Origin / Prism / Zotero，具体见下文 |

## 软件官方下载

| 软件 | 官方入口 | 下载 / 安装方法与核验 |
| --- | --- | --- |
| Python | [python.org 下载](https://www.python.org/downloads/) | Windows 选择合适的 64 位安装器；安装后运行 `python --version`。桌面科学软件建议使用独立环境，版本以 `originpro` 等包的实际支持为准 |
| Git（可选） | [git-scm.com 下载](https://git-scm.com/downloads/) | 用于 clone/更新仓库；不安装也可在 GitHub Code 菜单下载 ZIP |
| Node.js（DSH 安装需要） | [Node.js 下载](https://nodejs.org/en/download) | 选择官方当前支持版本；按 DeepSeek Harness 当期要求运行 npm/npx |
| Microsoft PowerPoint | [微软官方 PowerPoint](https://www.microsoft.com/microsoft-365/powerpoint) | 通过 Microsoft 365、学校/单位许可或已购 Office 安装桌面版；网页版不等于本机 COM/OLE |
| LibreOffice | [官方下载安装](https://www.libreoffice.org/download/) | 可用于部分 PPTX 渲染。不能替代 `ace-sci-origin` 的 Origin OLE 要求 |
| Origin / OriginPro | [OriginLab 下载/试用](https://www.originlab.com/demodownload.aspx) | 按试用、个人或学校许可下载安装；使用原生 Windows。详见 [软件桥说明](../skills/research-app-bridge/references/software.md) |
| GraphPad Prism | [GraphPad 官方入口](https://www.graphpad.com/scientific-software/prism/free-trial) | 按原厂试用/许可流程选择系统安装器；本项目命令启动器当前支持 Windows |
| Zotero | [Zotero 官方下载](https://www.zotero.org/download/) | 安装桌面端；需要本地检索时打开高级设置中的本机通信开关 |

## Agent 官方入口

| Agent | 获取方式 | 本仓库版本 |
| --- | --- | --- |
| Codex | [官方文档与产品入口](https://developers.openai.com/codex/) | [Codex 版](../editions/codex/README.md) |
| Claude Code | [官方安装说明](https://code.claude.com/docs/en/setup)；Windows 可用 `winget install Anthropic.ClaudeCode` | [Claude Code 版](../editions/claude-code/README.md) |
| DeepSeek Harness | [DeepSeek 官方仓库](https://github.com/deepseek-ai/deepseek-harness)；安装 Node.js 后按官方 `npx @deepseek-ai/dsh web` 启动 | [Harness 版](../editions/deepseek-harness/README.md) |
| WorkBuddy | [腾讯官方 WorkBuddy 页面](https://www.codebuddy.cn/work/)选择当前系统安装器 | [WorkBuddy 版](../editions/workbuddy/README.md) |
| 豆包 | [官方客户端下载](https://www.doubao.com/download/desktop) | [对话引导版](../editions/doubao/README.md)，不标称全自动本机执行 |

## Python 依赖

在独立环境中只安装所选技能的依赖：

```bash
python -m venv .venv
# Windows PowerShell：.venv/Scripts/Activate.ps1
# macOS/Linux：source .venv/bin/activate
python -m pip install -r skills/nature-paper2ppt/requirements.txt
# 使用对应技能时再安装其 requirements：
python -m pip install -r skills/nature-image2ppt/requirements.txt
python -m pip install -r skills/codex-ppt/requirements.txt
```

Origin 外部 Python 另按 [OriginLab 官方说明](https://docs.originlab.com/python)安装 `originpro`；Windows PowerPoint COM 通常使用 `pywin32`。安装 Python 包不会安装 Origin、Prism 或 PowerPoint。

验证普通软件路径与 Zotero 本地接口：

```bash
python skills/research-app-bridge/scripts/app_bridge.py doctor
python skills/nature-image2ppt/cli/image2ppt/cli.py doctor --json
```

前一个是共享环境诊断，后一个是图片重建自己的严格预检。二者不能互相替代。完整调用步骤见 [软件协作工作流](APP_WORKFLOWS.md)。
