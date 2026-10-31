# Claude Code 适配

本版面向具有本地文件与命令执行能力的 Claude Code（CLI 或桌面代码任务）。通过实际可用的 Read/Write、Bash/PowerShell 或等价工具执行步骤；不要调用并不存在的 Codex 工具名。技能可用 `/技能名` 或自然语言指定。

不要假定存在 Codex 内置生图或 Codex OAuth。图片生成/编辑需要宿主真实提供该能力，或配置兼容 Images API 的独立服务。`nature-image2ppt` 的非原生生图路线应明确选择 `openai-compatible-api`；密钥保存在本机配置/环境，不写入提示词和仓库。

Origin 和本项目 Prism 启动器要求原生 Windows。WSL、Claude 云端沙箱及普通网页对话不能直接操作本机桌面；此时改由本机命令桥执行，不能声称已操作应用。子 Agent 是否可用以宿主当前工具为准。
