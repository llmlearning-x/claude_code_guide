---
title: MCP 深度集成
---

# 第 10 章　MCP 深度集成：连接企业级数据

![MCP 深度集成：连接企业级数据](../images/mcp-deep-cover.png)

学会了写“Hello World”，现在我们要玩点真的。
在企业环境中，Claude Code 真正发挥价值的地方在于：**它可以直接访问你现有的数据孤岛**。

本章将通过三个进阶场景，展示如何将 MCP 集成到复杂的生产系统中：
1.  **数据库**：直接用自然语言查询 SQL。
2.  **API 网关**：通过 OpenAPI 规范自动生成 Server。
3.  **复杂状态**：处理分页、认证和上下文依赖。

## 10.1 场景一：连接 SQLite/PostgreSQL 数据库

想象一下，你对 Claude 说：“帮我找出上周注册的所有活跃用户，并按地区统计分布。”
如果没有 MCP，你得自己写 SQL，导出 CSV，粘贴给 Claude。
有了 MCP，Claude 可以直接查库。

### 10.1.1 官方 SQLite Server
MCP 官方维护了一个 `sqlite` 参考实现。我们可以直接使用它，而无需重写代码。

**安装与配置**：
```json
{
  "mcpServers": {
    "my-db": {
      "command": "uvx",
      "args": [
        "mcp-server-sqlite",
        "--db-path",
        "/path/to/my/production.db"
      ]
    }
  }
}
```
*(注：`uvx` 是 Python 工具链 `uv` 的执行命令，可以快速运行 Python 包。你也可以用 `pipx` 或 `docker`)*

### 10.1.2 安全性设计 (ReadOnly)
你肯定不希望 Claude 不小心删了库。
**最佳实践**：
- **只读账号**：为 MCP Server 创建一个专用的数据库用户，只授予 `SELECT` 权限。
- **Schema 过滤**：在 Server 代码中硬编码允许访问的表名列表，隐藏敏感表（如 `admin_users`, `secrets`）。

---

## 10.2 场景二：基于 OpenAPI (Swagger) 自动生成

你的公司可能有成百上千个微服务，每个都有 REST API。如果都要手写 MCP Server，那得累死。
好消息是：如果你的 API 有 OpenAPI (Swagger) 文档，你可以**自动生成 MCP Server**。

### 10.2.1 使用 `fastmcp` 或类似工具
社区已经涌现出许多“转换器”工具。以 Python 的 `fastmcp` 为例：

```python
from fastmcp import FastMCP

# 直接从 OpenAPI 文档 URL 创建 Server
mcp = FastMCP.from_openapi(
    url="https://api.my-company.com/openapi.json",
    name="company-api"
)

mcp.run()
```

### 10.2.2 自动生成的局限性
自动生成的工具通常缺乏“语义”。
- API 里的 `GET /users/{id}` 可能参数叫 `id`，但 Claude 不知道这个 ID 是 UUID 还是自增整数。
- **解决方案**：在 OpenAPI 文档中完善 `description` 字段。Claude 会读取这些描述作为 Prompt 的一部分。

---

## 10.3 场景三：处理分页与长列表 (Pagination)

MCP 的一个常见挑战是：数据量太大，Token 不够用。
比如你问：“列出所有 Jira Ticket”，Server 如果直接返回 10000 条记录，Claude 的上下文窗口瞬间就爆了。

### 10.3.1 资源分页 (Resource Pagination)
MCP 协议支持分页模式。
当 Claude 请求一个大资源时，Server 可以只返回前 100 条，并附带一个 `nextCursor`。
Claude Code 内部会自动处理这种分页逻辑（或者你可以明确告诉它“只读前 5 页”）。

### 10.3.2 摘要模式 (Summary Pattern)
与其返回原始数据，不如让 Server 先做一次“预处理”。
**Bad Tool**: `get_all_logs()` -> 返回 100MB 文本。
**Good Tool**: `analyze_logs(keyword, time_range)` -> Server 在本地 grep 后，只返回匹配的 50 行。

**设计原则**：**把计算留在 Server 端，把决策留给 Claude。**

---

## 10.4 认证与鉴权 (Authentication)

企业服务通常需要 API Key 或 OAuth Token。

### 10.4.1 环境变量注入
最简单的方式是通过环境变量传递密钥。
在 Claude Code 的配置文件中：

```json
{
  "mcpServers": {
    "github": {
      "command": "node",
      "args": ["index.js"],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
      }
    }
  }
}
```

### 10.4.2 动态 OAuth (Human-in-the-loop)
有些 Server 需要用户手动登录。
MCP 协议支持 Server 向 Host 发送“需要用户输入”的请求。
当 Server 启动时，它可以在日志中打印一个 URL：“请访问 `http://localhost:3000/auth` 进行登录”。用户在浏览器完成登录后，Server 获取 Token 并开始工作。

---

## 10.5 小结

深度集成不仅仅是“调通 API”，更是对**数据流向的设计**。
- 用 **Read-Only 账号** 保护数据库。
- 用 **OpenAPI** 批量接入微服务。
- 用 **预处理** 和 **分页** 解决 Token 瓶颈。

掌握了这些，你就可以把 Claude Code 变成一个真正的“全栈工程师”——它左手查库，右手调接口，中间还能帮你写总结报告。

在下一章，我们将讨论最后一个关键话题：**如何把这一切安全地部署到团队环境中**。
