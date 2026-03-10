---
title: Skill 设计模式与最佳实践
---

# 第 6 章　Skill 设计模式与最佳实践

![Skill 设计模式：常见架构与最佳实践](../images/skill-patterns-cover.png)

在第 5 章中，我们实现了一个简单的 `generate_commit_message` Skill。这就像学会了写“Hello World”函数。但在真实的工程体系中，Skill 往往需要处理更复杂的逻辑：多步推理、错误重试、条件分支等。

本章将介绍几种成熟的 **Skill 设计模式**。这些模式源自软件工程中的经典设计模式（如管道、策略、适配器），经过改造后，非常适合用于构建稳定、强大的 AI 能力。

## 6.1 Skill 设计的“三层模型”

在开始具体模式之前，我们先统一一下 Skill 的架构视图。一个健壮的 Skill 通常包含三个层次：

1.  **接口层 (Interface Layer)**：
    - 定义 `inputs`（参数）和 `outputs`（返回值）。
    - 负责参数的校验和默认值填充。
    - *类比：API 的 Controller 层。*

2.  **逻辑层 (Logic Layer / Prompt Strategy)**：
    - 决定如何组织 Prompt。
    - 决定是否需要分步骤调用 AI（Chain of Thought）。
    - 决定如何解析 AI 的原始回复。
    - *类比：Service 层。*

3.  **能力层 (Capability Layer)**：
    - 实际执行动作的地方（读文件、调 API、运行命令）。
    - 这一层往往依赖底层的 Claude Code 内置工具或 MCP 工具。
    - *类比：DAO / Infrastructure 层。*

设计 Skill 时，**逻辑层**是我们可以发挥最大创造力的地方。

---

## 6.2 常见 Skill 设计模式

### 6.2.1 管道模式 (The Pipeline)
**适用场景**：任务可以被拆分为线性步骤，每一步的输出是下一步的输入。

**案例**：`refactor_module`（模块重构）
1.  **Step 1 (Analyze)**：读取旧代码 -> 输出重构计划（JSON）。
2.  **Step 2 (Implement)**：读取重构计划 -> 输出新代码。
3.  **Step 3 (Verify)**：运行测试 -> 输出测试报告。

**Prompt 设计要点**：
- 显式要求 AI 在 Step 1 输出结构化数据（如 JSON），以便 Step 2 精确读取，避免“幻觉”传递。

### 6.2.2 路由模式 (The Router)
**适用场景**：用户的一个意图可能对应多种不同的处理路径。

**案例**：`analyze_log`（日志分析）
- 输入是一段日志。
- Skill 内部先进行一次快速判断（分类）：
    - 如果是 **SQL 错误** -> 调用 `sql_debugger` 子流程。
    - 如果是 **前端构建错误** -> 调用 `webpack_fixer` 子流程。
    - 如果是 **权限错误** -> 提示检查 IAM 配置。

**Prompt 设计要点**：
- 第一个 Prompt 专注于“分类”，不要尝试直接解决问题，输出类别标签即可。

### 6.2.3 验证器模式 (The Validator / Self-Correction)
**适用场景**：对输出的准确性要求极高（如生成 SQL、正则、JSON 配置）。

**案例**：`generate_sql`
1.  **Generate**：根据自然语言生成 SQL。
2.  **Validate**：在一个沙盒环境或通过 `EXPLAIN` 命令检查 SQL 语法。
3.  **Correct**：如果验证失败，将错误信息喂回给 AI：“你生成的 SQL 报错了，错误是...，请修正。”

**Prompt 设计要点**：
- 这是一个循环结构。需要设置最大重试次数（如 3 次），防止无限死循环。

---

## 6.3 Skill 的组合与嵌套

就像函数可以调用函数一样，Skill 也可以调用 Skill。

### 6.3.1 原子 Skill vs. 复合 Skill
- **原子 Skill**：只做一件事，不仅 Prompt 简单，而且容易测试。例如 `read_file`, `git_diff`, `parse_json`.
- **复合 Skill**：通过编排多个原子 Skill 来完成业务目标。例如 `daily_report` 可能内部调用了 `git_log_summary` 和 `ticket_system_query`。

### 6.3.2 组合的原则
- **依赖倒置**：复合 Skill 不应强依赖具体的原子 Skill 实现，而是依赖其“接口约定”。
- **上下文传递**：在 Skill 之间传递数据时，尽量清洗掉无关信息，只传核心字段，节省 Context Window。

---

## 6.4 Skill 与团队规范的结合

Skill 是推行团队规范的最佳载体。

### 6.4.1 风格指南即 Prompt
不要指望开发者去读那份 50 页的《编码规范 PDF》。把规范写进 Skill 的 System Prompt 里。
- **Naming Skill**：自动检查变量命名是否符合 `CamelCase` 或 `snake_case` 要求。
- **Linting Skill**：在生成代码时，强制要求 AI 遵守 Prettier 配置。

### 6.4.2 审查清单 (Checklist)
在 `code_review` Skill 中，内置团队关注的特定风险点：
- “是否包含硬编码的密钥？”
- “是否处理了 API 超时？”
- “是否打印了敏感日志？”

通过将这些检查点硬编码在 Prompt 中，Skill 成为了一个不知疲倦的、严格的审查员。

---

## 6.5 小结

设计 Skill 不仅仅是写 Prompt，更是在设计**微型软件系统**。
- 用 **三层模型** 隔离变化。
- 用 **管道、路由、验证器** 解决复杂逻辑。
- 用 **组合** 提高复用性。

当你掌握了这些模式，你就不再只是在使用 Claude Code，而是在**架构**它。你的 Skill 库将变得像标准库一样可靠。

下一章，我们将把视角放大，看看如何在一个多人团队中管理和分发这些 Skill，建立真正的**团队级 Skill 体系**。
