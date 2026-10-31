# 跨 Agent 调用科研软件

共用入口为 [research-app-bridge](../skills/research-app-bridge/SKILL.md)。安装到任意 Agent 后，将命令中的路径替换成实际技能目录；不要求存在 `origin_launch`、`prism_*` 或 `zotero_*` 等宿主专用工具。

## 1. 从文献到汇报

先打开 Zotero 并启用本机通信，再运行：

```bash
python skills/research-app-bridge/scripts/app_bridge.py zotero search --query "food protein" --limit 10
python skills/research-app-bridge/scripts/app_bridge.py zotero item --key ABCD1234
python skills/research-app-bridge/scripts/app_bridge.py zotero export --keys ABCD1234 --format bibtex --out ./task/references.bib
```

示例 key 必须换成实际检索结果。核对论文元数据与正文后，用 `nature-paper2ppt` 生成汇报；本地 API 检索结果不能替代全文内容。软件桥只读资料库。

## 2. 从真实数据到 Origin 图组

先按 `ace-sci-origin` 建立数据清单、Python/R 参考与样式契约。由 Agent 写出实际 Origin 构图脚本，再运行：

```bash
python skills/research-app-bridge/scripts/app_bridge.py origin run --script ./task/build_origin.py --expect ./task/figure.opju --expect ./task/figure.png
```

检查原生图页、轴、线宽、图例和预览，再进行 PowerPoint OLE 图组排版与验证。软件桥负责调用与产物检查，不自动替代面板的具体 Origin 实现。

## 3. 从已有 Prism 项目导出图形

```bash
python skills/research-app-bridge/scripts/app_bridge.py prism prepare-export --project ./input/source.pzfx --out-dir ./task/prism --graph 1
python skills/research-app-bridge/scripts/app_bridge.py prism run --script ./task/prism/export.pzc --expect ./task/prism/graph.pdf --expect ./task/prism/graph.png --expect ./task/prism/done.txt
```

前一步复制工程，生成官方 `.pzc` 命令；后一步用 `Prism.exe @script.pzc` 启动并等待产物。默认不覆盖源工程，不选择统计检验，也不新增虚构分析。需要重跑时选择新的空输出目录。

## 4. 给其他 Agent 的开场语

```text
使用 research-app-bridge，先运行 doctor 并说明你实际能访问的主机与软件。
根据当前任务选择 Origin、Prism 或 Zotero 工作流，在任务目录中操作副本。
调用后给出实际文件、接口响应和预览检查；缺少执行能力时给出可复制命令，不声称已经运行。
```

详细接口依据与失败处理分别见 [Origin](../skills/research-app-bridge/references/origin.md)、[Prism](../skills/research-app-bridge/references/prism.md)、[Zotero](../skills/research-app-bridge/references/zotero.md)。
