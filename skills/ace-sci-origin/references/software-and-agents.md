# 软件与 Agent 运行要求

需要原生 Windows、获许可的 Origin/OriginPro 和 Microsoft PowerPoint；外部 Python 使用 originpro，PPT COM 自动化通常还需 pywin32。LibreOffice 不能替代此技能的 Origin OLE 验证。先检查实际 COM 连接与软件许可。

官方下载、安装方法与按任务选择软件见 [软件指南](https://github.com/Medal-Pan/research-ppt-skills/blob/main/docs/SOFTWARE.md)。Agent 版本选择见 [适配指南](https://github.com/Medal-Pan/research-ppt-skills/blob/main/docs/AGENTS.md)。

安装技能目录不会安装桌面软件、取得软件许可或自动授予桌面访问权限。应使用实际执行任务的 Python 环境；本机 Origin 与本项目 Prism 启动器不在 WSL/云端 Python 中运行。
