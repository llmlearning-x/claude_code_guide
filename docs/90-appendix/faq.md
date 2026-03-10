---
title: 附录 D：常见问题与排错指南
---

# 附录 D　常见问题与排错指南

![附录：常见问题解答与排错指南](../images/appendix-faq-cover.png)

## D.1 Claude Code 使用 FAQ

**Q: Claude Code 的响应速度突然变慢了？**
A: 这通常是因为上下文（Context）太大了。Claude 会读取你最近打开的所有文件和终端输出。
**解决方案**：
1.  运行 `/reset` 或 `/clear` 命令清除上下文。
2.  使用 `.claudeignore` 排除不必要的大文件（如 `package-lock.json` 或 `dist/`）。

**Q: 如何中断 Claude 正在执行的长任务？**
A: 在终端按 `Ctrl+C`。这会立即停止当前的生成或工具执行。

**Q: Claude 修改了我的代码，但我不想接受，怎么办？**
A: 如果你在 Plan Mode 下，直接拒绝即可。如果已经执行了，Claude Code 通常会自动为你创建一个 Git 提交。你可以使用 `git reset --hard HEAD~1` 回滚。
**建议**：始终在一个干净的 Git 分支上运行 Claude。

**Q: 为什么 Claude 总是找不到我的文件？**
A: 请检查你的工作目录（CWD）。Claude 默认只能看到当前目录下的文件。如果文件在子目录中，请使用相对路径。另外，检查该文件是否被 `.gitignore` 或 `.claudeignore` 忽略了。

## D.2 Skill 与 MCP 开发 FAQ

**Q: 我配置了 MCP Server，但 Claude 说“找不到工具”？**
A: 排查步骤：
1.  检查 `claude_config.json` 中的命令路径是否正确（建议使用绝对路径）。
2.  检查 Server 是否正常启动。你可以尝试手动运行该命令，看是否有报错。
3.  如果是 Python Server，确保虚拟环境已激活，或使用 `uvx` / `pipx` 运行。
4.  重启 Claude Code（配置更改需要重启生效）。

**Q: 本地开发的 MCP Server 如何调试？**
A: 使用 MCP Inspector。
1.  运行 `npx @modelcontextprotocol/inspector <你的 server 命令>`。
2.  在浏览器中打开 Inspector 提供的 URL。
3.  你可以在网页上模拟发送请求，查看 Server 的响应日志。

**Q: 遇到 `Connection refused` 或 `EADDRINUSE` 错误？**
A: 这通常发生在基于 HTTP/SSE 的 Server 上。
-   确保端口没有被占用。
-   确保防火墙允许该端口的本地连接。
-   如果是 Docker 运行的 Server，检查端口映射 `-p` 参数。

**Q: Claude 执行 SQL 时总是超时？**
A: 默认情况下，MCP 工具的执行时间是有限制的。对于慢查询：
1.  优化 SQL 语句（添加索引）。
2.  在 Server 代码中增加超时时间设置。
3.  让 Claude 分页查询（`LIMIT 100`）。
