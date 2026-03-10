---
title: 附录 C：术语表
---

# 附录 C　术语表（Glossary）

![附录：术语表与概念解释](../images/appendix-glossary-cover.png)

## C.1 Claude Code 相关术语

**Agent (代理)**
在 AI 语境下，指不仅能生成文本，还能通过工具（Tools）与外部环境交互、自主执行任务的智能实体。Claude Code 具有 Agent 的特性。

**Context Window (上下文窗口)**
LLM 一次能处理的最大 Token 数量。Claude 3.5 Sonnet 拥有 200k Token 的上下文窗口，这使得它能一次性读取大量代码文件。

**REPL (Read-Eval-Print Loop)**
“读取-求值-输出”循环。Claude Code 的交互模式本质上是一个增强版的 REPL，用户输入指令，Claude 执行并返回结果。

**Plan Mode (计划模式)**
Claude Code 的一种工作模式。在此模式下，Claude 会先生成详细的执行计划，待用户确认后才开始修改文件。适用于复杂或高风险任务。

**CLAUDE.md**
项目根目录下的特殊配置文件。用于定义项目的上下文、常用命令（Skill）和代码风格规范。Claude 每次启动时都会读取它。

## C.2 Skill 相关术语

**Skill (技能)**
Claude Code 可调用的自定义工具。通常封装了 Shell 命令或脚本。定义在 `CLAUDE.md` 或全局配置中。

**Tool Use (工具调用)**
LLM 的一种能力，指模型能够生成特定格式的输出来调用预定义的函数或 API。

**Schema (模式)**
用于描述数据结构的规范（通常是 JSON Schema）。在定义 Skill 时，用于描述参数的类型和格式。

## C.3 MCP 与协议相关术语

**MCP (Model Context Protocol)**
一种开放标准协议，旨在标准化 AI 模型与外部数据源（如数据库、API、本地文件）之间的连接方式。

**Host (宿主)**
运行 LLM 的应用程序，如 Claude Desktop App、Claude Code CLI 或 Cursor。Host 负责发起连接请求。

**Server (服务端)**
MCP 架构中的数据提供方。它通过标准协议暴露 Resources（资源）、Prompts（提示词）和 Tools（工具）。

**Client (客户端)**
MCP 架构中连接 Host 和 Server 的组件。在 Claude Code 中，CLI 本身充当了 Client 的角色。

**Resource (资源)**
MCP 中的一种数据类型，代表可读取的数据块（如文件内容、数据库记录）。类似于 HTTP 中的 GET 请求。

**Transport (传输层)**
MCP 通信的底层通道。目前主要支持 Stdio（标准输入输出）和 SSE（Server-Sent Events）。
