# 发布检查记录

检查日期：2026-10-30。范围：本地发布目录，版本 `0.1.0`。

已完成：

- 五个技能入口均通过 `skill-creator` 的格式检查。
- 技能目录、各自许可证、论文汇报 manifest 的引用文件与图片重建运行入口均存在。
- 80 个 Python 文件通过语法解析；JSON 与 SVG 内容通过解析；Markdown 实际本地链接可解析。
- 按私有配置文件名、常见 GitHub/API 令牌格式和个人绝对路径扫描，未发现命中。
- 在隔离的临时目标目录实际安装轻量图片复现技能，安装文件哈希与发布文件一致。
- 已有同名技能时安装器拒绝覆盖；多技能请求在预检失败时不会先安装其他技能。
- 未将本机实验目录、生成的 PPT/PDF/Origin 工程、缓存或真实配置收入发布目录。

验证命令：

```bash
python scripts/validate_repository.py
python scripts/install_skills.py --skill image-to-editable-ppt --dest <临时技能目录>
```

本记录不表示已完成全部技能的端到端制作、生图服务验证、Origin/PowerPoint 自动化或跨平台视觉验收。GitHub Actions 配置已经随包提供，其远端执行结果需在仓库发布后确认。
