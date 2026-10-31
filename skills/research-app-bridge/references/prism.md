# GraphPad Prism：项目副本与官方脚本

前提：已安装且获许可的 GraphPad Prism。当前命令启动器针对原生 Windows，未在所有 Prism 版本实测。

先准备用户已有、已确认分析设计的项目或模板。下面的命令复制项目，生成导出第 1 张图的脚本，不修改原文件，也不自行选择统计检验：

```bash
python <SKILL>/scripts/app_bridge.py prism prepare-export --project ./input/source.pzfx --out-dir ./task/prism --graph 1
python <SKILL>/scripts/app_bridge.py prism run --script ./task/prism/export.pzc --expect ./task/prism/graph.pdf --expect ./task/prism/graph.png --expect ./task/prism/done.txt
```

若无法找到程序，设置 `PRISM_EXE` 或传入 `--exe`。旧版 Prism 对文件编码和非 ASCII 路径的支持可能不同，失败时使用简短英文任务路径重试，不修改系统文件关联。

Windows 官方命令行为 `Prism.exe @脚本路径`，`@` 必须保留。脚本的图号从 1 开始；`GoTo G, 1` 选择第一张图，`ExportPDF` / `ExportPNG` 导出。进程启动是异步的，必须检查新生成的导出文件或完成标记。

新增分析时，先确定数据表类型、重复结构、缺失值与分析方法，再由用户项目/可靠模板承载分析。不要伪造 `.prism`、`.pzf` 或结果页。不能完成原生分析时，报告具体限制及已经生成的文件。

macOS 用户可按官方 AppleScript/Automator 路线运行 `.pzc`；本仓库不把 Windows 启动器标称为 macOS 自动化实现。

依据：[Windows 脚本启动](https://www.graphpad.com/guides/prism/latest/user-guide/launching_a_prism_script_from_outside_prism_%28windows%29.htm)、[页面定位命令](https://www.graphpad.com/guides/prism/latest/user-guide/general_commands.htm)、[导出命令](https://www.graphpad.com/guides/prism/latest/user-guide/exporting_a_graph_or_layout.htm)、[macOS 脚本路线](https://www.graphpad.com/guides/prism/latest/user-guide/launching_prism_from_applescript.htm)。
