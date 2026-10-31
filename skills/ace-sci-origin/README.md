# ace-sci-origin

面向高质量科研绘图工作流的 Codex Skill：以 Python/R 参考图为视觉契约，将电子表格数据转换为可编辑的 Origin 工程，并生成包含 Origin OLE 对象的 PowerPoint 组合图。

## 项目信息

- 作者：研理科研线
- 类型：Codex Skill
- 许可证：MIT
- 适用平台：Windows（OriginPro 与 Microsoft PowerPoint 自动化）

## 主要能力

- 检查 Excel 工作簿中的工作表、字段、单位和数据结构。
- 生成确定性的 Python/R 参考图及逐面板样式契约。
- 创建可编辑的 Origin `.opju` 工程和原生图页。
- 强制执行坐标轴、刻度、线宽、颜色、图例和版式规范。
- 将 Origin 图页以 OLE 对象写入 PowerPoint，保持双击编辑能力。
- 在 PPT 中完成多面板排版和面板字母标注。
- 导出预览并执行参考图、Origin 和 PowerPoint 之间的视觉与结构检查。

## 设计原则

1. Python/R 参考图是视觉标准，Origin 是可编辑渲染后端。
2. 普通二维图必须使用 Origin 原生坐标轴，不能用线对象伪造。
3. Origin 图页保持干净，面板字母默认在 PowerPoint 中添加。
4. 多序列图必须显式设置颜色、线宽和图例，不能保留 Origin 默认样式。
5. 发布前必须检查 Origin 预览、PPT 预览、OLE 对象和最终状态报告。

完整规则见 [`SKILL.md`](SKILL.md)，专项规范位于 [`references/`](references/)。

## 安装

将仓库克隆到 Codex skills 目录：

```powershell
git clone https://github.com/hzsci/ace-sci-origin.git "$env:USERPROFILE\.codex\skills\ace-sci-origin"
```

重新启动 Codex 或刷新技能列表后即可使用。

也可以下载仓库压缩包，解压后确保目录结构如下：

```text
~/.codex/skills/ace-sci-origin/
├── SKILL.md
├── agents/
└── references/
```

## 使用方式

在 Codex 中明确指定该 Skill，并提供需要处理的 Excel 工作簿或参考图。例如：

```text
使用 ace-sci-origin 处理当前文件夹中的 Figure 3 数据，生成 Python 参考图、可编辑 Origin 工程和带 OLE 对象的 PowerPoint 组合图。
```

典型输出包括：

- Python/R 参考图；
- 面板级样式契约；
- 可编辑 Origin `.opju` 工程；
- Origin 面板预览；
- 包含 Origin OLE 对象的 `.pptx`；
- PPT 预览和验证报告；
- `generation_status.json`。

## 环境要求

- Windows；
- Origin/OriginPro，并支持 Python 或 COM 自动化；
- Microsoft PowerPoint；
- Python 及绘图、表格处理依赖；
- 若使用 R 参考图，需要本机安装对应 R 环境。

本 Skill 会主动检查并尝试连接 Origin。若部分自动化能力不可用，应保留已生成的稳定成果，并在状态报告中记录准确的失败原因。

## 仓库结构

```text
ace-sci-origin/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
└── references/
    ├── excel-python-origin-ole-workflow.md
    ├── nature-style-origin.md
    ├── origin-axis-contract.md
    ├── origin-ppt-pitfalls.md
    ├── origin-style-contract.md
    └── reference-first-origin.md
```

## 贡献

欢迎通过 Issue 报告 Origin 版本兼容问题、OLE 渲染差异或版式复现问题，也欢迎提交 Pull Request 改进工作流规范。

提交修改时，请确保不降低 `SKILL.md` 中对原生坐标轴、参考图匹配、OLE 可编辑性和验证报告的要求。

## 许可证

本项目采用 [MIT License](LICENSE) 开源。

