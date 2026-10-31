# 安装与环境

先按 [Agent 版本](AGENTS.md)选择安装或导入方式，再看 [软件与官方下载](SOFTWARE.md)。完整版本包见仓库 Releases；本机软件协作见 [快捷工作流](APP_WORKFLOWS.md)。

## 技能文件

需要 Python 3.10 或更高版本来运行本仓库安装脚本。它仅使用标准库，不要求先安装全部制作依赖。

```bash
python scripts/install_skills.py --skill image-to-editable-ppt --dry-run
python scripts/install_skills.py --skill image-to-editable-ppt
```

不传 `--skill` 或 `--all` 会显示用法。已有同名目录时安装会停止，避免覆盖个人调优；请先自行备份或改用其他 `--dest`。

安装位置由 `--dest` 优先指定；也可用 `--project` 选择项目级目录。当前 Codex 默认 `~/.agents/skills`，Claude Code 默认 `~/.claude/skills`，DeepSeek Harness 默认 `$DSH_HOME/skills` 或 `~/.dsh/skills`。WorkBuddy/豆包导出到指定目录后按相应说明使用；不猜测其内部目录。安装后让宿主重新加载技能列表。

## 按需安装依赖

以下命令在仓库根目录运行。建议在独立 Python 虚拟环境中操作。没有使用某技能时，无须安装其依赖。

| 技能 | 依赖及预检 |
| --- | --- |
| `image-to-editable-ppt` | 由宿主提供图片查看、PPTX 写出和预览能力；未绑定固定制作库 |
| `nature-paper2ppt` | `python -m pip install -r skills/nature-paper2ppt/requirements.txt`；包体检查脚本仅使用标准库 |
| `nature-image2ppt` | `python -m pip install -r skills/nature-image2ppt/requirements.txt`，然后 `python skills/nature-image2ppt/cli/image2ppt/cli.py doctor --json`；预检成功后开始任务 |
| `codex-ppt` | `python -m pip install -r skills/codex-ppt/requirements.txt`；还需宿主生图能力或所选兼容服务，样张与后端流程见技能 |
| `ace-sci-origin` | Windows、可调用的 Origin/OriginPro 与 Microsoft PowerPoint，详见该技能说明；软件本身不随包分发 |
| `research-app-bridge` | Python 标准库命令桥；Origin 任务另需 `originpro` 与本机 Origin，Prism 任务需 Prism，Zotero 检索需其本地 API |

复制到宿主目录后，命令中的 `skills/<名称>` 应替换为实际安装目录。制作时使用同一个 Python 环境；本仓库安装脚本不会为宿主切换解释器。

`nature-image2ppt` 的渲染依赖 PowerPoint 或 LibreOffice，公式页面还可能需要 TeX 等工具，具体以 `doctor` 和任务内容为准。缺少渲染能力时，不能把包体检查称为视觉验收。

## 配置与材料

仅复制示例配置并在本机填写。真实 `.env`、`config.yaml`、令牌与论文/实验输入不应提交到仓库。不要把 Codex OAuth 凭据填写到第三方生图服务；第三方服务使用它自己的凭据与端点。

涉及在线生图、编辑或 OCR 时，先确认该材料允许发送到所选服务。详细配置遵从各技能自带说明。
