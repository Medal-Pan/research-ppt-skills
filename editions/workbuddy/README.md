# WorkBuddy 版

从 [官方 WorkBuddy 页面](https://www.codebuddy.cn/work/) 下载安装客户端。此版不猜测其内部技能目录。

```bash
python scripts/build_editions.py --agent workbuddy
```

在 `dist/workbuddy/` 得到六个单技能 ZIP。按 [WorkBuddy 官方技能说明](https://open.workbuddy.cn/docs/skill)进入“专家·技能·连接器 → 技能 → 添加技能”，使用当前版本提供的创建/上传入口导入一个 ZIP；不要把含六个技能的整仓库 ZIP 当成一个技能上传。

如只需导出适配后的文件夹，可用 `python scripts/install_skills.py --agent workbuddy --all --dest ./workbuddy-import`。本版补齐官方展示字段，但不代表已通过 WorkBuddy 市场上架审核或所有客户端版本实测。
