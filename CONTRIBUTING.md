# 贡献说明

提交问题时，请说明技能名称、操作系统、Python/宿主版本、最小复现步骤，以及实际结果与期望结果。公开材料前移除令牌和未授权数据。

修改第三方技能时保留许可证和署名，说明与上游的差异；修改 Apache-2.0 来源文件时在文件内注明改动。新增技能应包含有效的 `SKILL.md`，并在 `skills.json` 登记来源、许可证和平台边界。

提交前运行：

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repository.py
```

结构检查不能替代实际制作品质验证。涉及 PPTX 生成或图片重建行为时，提供可公开的最小输入、实际输出和渲染/检查证据；不要仅提供代码执行成功的截图。
