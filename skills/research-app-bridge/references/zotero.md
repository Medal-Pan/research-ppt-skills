# Zotero：本地检索与引用导出

打开 Zotero，在设置 → 高级中启用“允许本机其他应用与 Zotero 通信”。本工具仅向 `127.0.0.1` 发送 GET 请求，不修改资料库，也不读取 SQLite 文件。

```bash
python <SKILL>/scripts/app_bridge.py zotero ping
python <SKILL>/scripts/app_bridge.py zotero search --query "food protein" --limit 10
python <SKILL>/scripts/app_bridge.py zotero item --key ABCD1234
python <SKILL>/scripts/app_bridge.py zotero export --keys ABCD1234 EFGH5678 --format ris --out ./task/selected.ris
```

先根据搜索返回的真实 key 取详情，核对题名、作者、年份与 DOI，再导出 RIS 或 BibTeX。示例 key 是占位符，不是可引用的文献。若 API 返回 403，检查本地 API 开关；连接拒绝时检查 Zotero 是否运行。云端 Agent 无法直接访问用户电脑的 localhost，应改用本地宿主执行或由用户提供导出结果。

需要入库时，可生成待核验的 RIS/BibTeX 后用 Zotero 的文件导入功能处理。此只读桥不提供写入授权或资料库变更接口。支持 Zotero 本地 API 的版本方可使用；Zotero 10 的写入接口另有正式授权要求，不应复用网页 API key 或绕过确认。

依据：[本地 API](https://www.zotero.org/support/dev/web_api/v3/local_api)、[检索与导出参数](https://www.zotero.org/support/dev/web_api/v3/basics)。
