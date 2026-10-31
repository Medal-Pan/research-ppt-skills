# DeepSeek Harness 适配

本版使用标准 `SKILL.md` 目录包，交由 Harness 的本地 skills provider 加载。用已加载的文件系统、终端、浏览器等插件执行步骤，不假定 Codex 的工具或权限存在。项目级目录为 `.dsh/skills`；用户目录可由 `DSH_HOME` 指定。

先检查当前 Harness 组合是否提供读写文件、运行命令、查看图片和按需生图的能力。Harness 的网页界面并不等于纯云聊天；运行时所在的主机才决定能否访问桌面软件和 localhost。

图片服务使用宿主生图插件或兼容 API，不读取 Codex OAuth。Origin/Prism 在本机原生 Windows 调用；Zotero 用同机本地 API。缺少工具时说明缺项并给出本机命令，不把脚本建议称为执行结果。
