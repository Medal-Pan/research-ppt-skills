# Origin：外部 Python 工作流

前提：原生 Windows、已安装且获许可的 Origin/OriginPro、与自动化环境匹配的 Python。`originpro` 连接实际 Origin，不能用普通图片生成代替。

```bash
python -m pip install originpro
python <SKILL>/scripts/app_bridge.py doctor
python <SKILL>/scripts/app_bridge.py origin run --script ./task/build_origin.py --expect ./task/figure.opju --expect ./task/figure.png
```

任务脚本应读取用户真实数据，连接其自身创建的 Origin 实例，在其中建表、作图并保存到任务输出目录。外部 Python 的基本 API 为 `import originpro as op`、`op.set_show(True)`、`op.open(file=..., readonly=True)`、`op.save(...)`；结束时只关闭本脚本拥有的实例。不要默认附着并清空用户正在编辑的项目。

从参考图生成图组时，先建立样式契约，再运行按面板编写的 Origin 脚本。保存原生图页，检查坐标轴、线宽、颜色、图例和预览；需要 OLE 图组时继续执行 `ace-sci-origin` 的 PowerPoint 排版与验证规则。

`origin run` 只负责运行已写好的任务脚本和核对预期文件，不能把一个空白脚本变成绘图实现。宿主中的 `origin_launch` / `origin_run_python` 等工具可用时也可使用，但其他 Agent 不应假定这些工具一定存在。

依据：[OriginLab 外部 Python 示例](https://docs.originlab.com/externalpython/external-python-code-samples/)、[Python 接口说明](https://docs.originlab.com/python)。
