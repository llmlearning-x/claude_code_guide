---
title: MCP 安全与部署
---

# 第 11 章　MCP 安全与部署：从本地到生产

![MCP 安全与部署：从本地到生产](../images/mcp-security-cover.png)

当你开发了一个强大的 MCP Server，你的第一反应可能是：“太棒了，我要把它分享给全公司！”
但等等，如果这个 Server 连接了生产数据库，或者可以执行 `kubectl delete`，你真的敢直接让它上线吗？

本章将讨论 MCP 的**安全边界**和**部署策略**，确保你在享受 AI 带来的便利时，不会炸掉生产环境。

## 11.1 安全原则：零信任与最小权限

### 11.1.1 永远不要信任 LLM
尽管 Claude 很聪明，但它偶尔也会产生“幻觉”。
- 它可能会编造一个不存在的 SQL 表名。
- 它可能会在删除文件时“手滑”多删了一个字符。

**原则**：**Server 端必须进行严格的输入校验。**
- 使用 `zod` 或 `pydantic` 校验所有参数。
- 不要把 SQL 拼接交给 Claude，必须使用参数化查询。

### 11.1.2 最小权限 (Least Privilege)
如果你的 Server 只需要读取数据，就不要给它写入权限。
- **数据库**：使用 Read-Only 账号。
- **文件系统**：限制只能访问特定目录（如 `/tmp/sandbox`），严禁访问 `/etc` 或 `~/.ssh`。
- **网络**：限制只能访问白名单域名。

---

## 11.2 部署策略：本地、Docker 与 Serverless

MCP Server 本质上是一个进程，你可以用多种方式运行它。

### 11.2.1 方案 A：本地运行 (Localhost)
**适用场景**：个人开发、访问本地文件/数据库。
**优点**：零延迟，直接访问本地环境。
**缺点**：只能你自己用，无法共享。

```bash
# Claude Config
"command": "node",
"args": ["/Users/me/projects/my-server/index.js"]
```

### 11.2.2 方案 B：Docker 容器 (推荐)
**适用场景**：团队共享、需要隔离环境。
你可以把 Server 打包成 Docker 镜像，通过 `docker run` 运行。

```bash
# Claude Config
"command": "docker",
"args": [
  "run",
  "-i",
  "--rm",
  "-v", "/data:/data",
  "my-company/mcp-server:latest"
]
```
**优点**：环境一致，便于分发，且通过 Docker 限制了文件系统权限。

### 11.2.3 方案 C：Serverless / 远程部署 (Remote MCP)
**适用场景**：SaaS 服务集成、无需访问本地资源。
目前 MCP 主要支持 Stdio 通信，但社区正在探索基于 SSE (Server-Sent Events) 或 WebSocket 的远程协议。
一旦成熟，你可以把 Server 部署在 AWS Lambda 或 Cloudflare Workers 上，Claude 通过 HTTP 连接。

---

## 11.3 审计与监控 (Auditing)

当 AI 开始操作你的系统时，你必须知道它到底干了什么。

### 11.3.1 日志记录
MCP Server 的所有操作都应该记录日志。
- **Who**：哪个用户（如果支持多用户）。
- **What**：调用了哪个工具，参数是什么。
- **Result**：成功还是失败。

### 11.3.2 敏感操作审批
对于高风险操作（如 `deploy_prod`, `refund_money`），可以在 Server 内部实现“二次确认”逻辑。
或者利用 Claude Code 本身的 `y/N` 确认机制，在工具描述中注明：“此操作将产生副作用，请谨慎执行。”

---

## 11.4 小结：构建可信赖的 AI 基础设施

MCP 是连接 AI 与现实世界的桥梁，而安全是这座桥梁的护栏。
- **校验输入**，防止注入攻击。
- **限制权限**，防止意外破坏。
- **容器化部署**，隔离运行环境。
- **审计日志**，追踪每一次调用。

至此，我们已经完成了 MCP 部分的学习。你不仅学会了如何写 Server，还学会了如何安全地管理它们。

在接下来的 **第 IV 部分**，我们将进入实战环节。我们将把前面学到的 **Claude Code 基础**、**Skill** 和 **MCP** 全部结合起来，解决真实的工程难题。
