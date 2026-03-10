---
title: 附录 A：Prompt 模板索引
outline: deep
---

# 附录 A　Prompt 模板索引

![附录：Prompt 模板索引与参考](../images/appendix-prompt-cover.png)

本附录整理了书中各章节提到的关键 Prompt，以及在实际开发中经过验证的高效指令。你可以直接复制这些 Prompt，根据你的项目上下文稍作修改即可使用。

## A.1 Claude Code 基础 Prompt

### 项目初始化 (Project Initialization)
用于快速搭建项目骨架。

> **Prompt**:
> "请使用 [技术栈，例如 Vite + React + TypeScript] 初始化一个名为 [项目名称] 的新项目。安装 [关键依赖，例如 Tailwind CSS, Zustand] 并配置好基础样式。请确保项目结构符合最佳实践。"

### 代码解释 (Code Explanation)
用于理解复杂的遗留代码。

> **Prompt**:
> "请阅读 `[文件路径]`。解释 `[函数名或类名]` 的核心逻辑。请使用 Mermaid 绘制其时序图，展示数据流向。如果是你来重构这段代码，你会怎么做？"

### 单元测试生成 (Test Generation)
用于为现有代码补充测试。

> **Prompt**:
> "请为 `[文件路径]` 中的 `[函数名]` 编写单元测试。使用 [测试框架，例如 Vitest]。请覆盖正常情况、边界情况（如空输入、极大值）以及异常处理路径。不要修改原代码，只生成测试文件。"

### 提交信息生成 (Commit Message)
用于生成规范的 Git 提交信息。

> **Prompt**:
> "请分析我刚才的修改（运行 `git diff`）。生成一条符合 Conventional Commits 规范的提交信息。格式应为：`<type>(<scope>): <subject>`，并包含详细的 Body 解释修改原因。"

## A.2 Skill 设计 Prompt

### Skill 定义生成 (Skill Definition)
用于让 Claude 帮你写 `CLAUDE.md` 中的 Skill 定义。

> **Prompt**:
> "我想创建一个名为 `[Skill 名称]` 的 Skill，它的功能是 `[功能描述]`。它需要接受 `[参数列表]` 作为输入。请为我生成对应的 `CLAUDE.md` 配置代码，包括 `description` 和 `cmd` 字段。"

### 复杂命令封装 (Command Wrapping)
用于将复杂的 Shell 命令封装为 Skill。

> **Prompt**:
> "请将以下命令封装为一个名为 `deploy-prod` 的 Skill：`[复杂命令，例如 ./deploy.sh --env=prod --key=$KEY]`。请确保它能从环境变量中读取密钥，并且在执行前要求用户确认。"

## A.3 MCP 开发 Prompt

### MCP Server 脚手架 (Server Scaffolding)
用于快速创建 MCP Server。

> **Prompt**:
> "请使用 TypeScript 和 `@modelcontextprotocol/sdk` 创建一个 MCP Server。它应该包含一个名为 `[工具名]` 的 Tool，用于 `[工具功能]`。请生成 `index.ts`、`package.json` 和 `tsconfig.json`。"

### SQL 查询生成 (SQL Generation via MCP)
用于通过 `sqlite` MCP Server 查询数据。

> **Prompt**:
> "请连接到 `[数据库路径]`。查询 `[表名]` 表，找出 `[条件，例如最近 7 天注册的用户]`。请按 `[字段]` 排序并只返回前 10 条。请先告诉我你要执行的 SQL，再执行。"

### API 适配器生成 (API Adapter)
用于将外部 API 转换为 MCP Tool。

> **Prompt**:
> "请阅读 `[OpenAPI 文档 URL]`。为其中的 `[API 路径]` 端点创建一个 MCP Tool 定义。请提取所有必需参数，并为每个参数添加详细的描述，以便 LLM 理解。"

## A.4 团队协作 Prompt

### 代码审查 (Code Review)
用于让 Claude 扮演审查者。

> **Prompt**:
> "请作为一名资深 [语言] 工程师审查 `[文件路径]`。关注以下几点：1. 安全性（是否存在注入风险）；2. 性能（是否有不必要的循环）；3. 可读性（命名是否规范）。请以列表形式给出具体的修改建议。"

### 文档生成 (Documentation)
用于生成项目文档。

> **Prompt**:
> "请阅读当前目录下的所有代码。生成一份 `README.md`，包含：项目简介、安装步骤、核心功能列表、配置说明。请使用 Markdown 格式，并包含适当的代码块示例。"

### 架构决策记录 (ADR Generation)
用于记录技术决策。

> **Prompt**:
> "我们刚才决定使用 `[技术 A]` 而不是 `[技术 B]` 来实现 `[功能]`。请帮我撰写一份 ADR (Architecture Decision Record)，记录背景、选择理由、被否决的方案以及潜在的后果。"
