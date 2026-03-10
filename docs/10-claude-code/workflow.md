---
title: Claude Code 工作流
---

# 第 3 章　把 Claude Code 嵌入你的日常工作

![日常工作流：从需求分析到代码交付](../images/cc-workflow-cover.png)

了解了 Ask、Plan、Agent 和 Debug 四种模式后，下一个问题是：**我该怎么把它们串起来，用到我每天的搬砖生活里？**

本章将从“环境搭建”开始，一步步带你构建一个基于 Claude Code 的高效开发工作流。我们的目标不是让你变成“只会写 Prompt 的人”，而是让你现有的工作流（Git、IDE、CI/CD）因为有了 AI 而变得更快、更稳。

## 3.1 搭建最小可用环境

在正式开始之前，确保你的工程环境已经准备就绪。

### 3.1.1 忽略文件配置
Claude Code 会读取你的项目文件，但有些文件（如 `package-lock.json`、巨型数据文件、敏感配置）是不应该被读取的。
虽然 Claude Code 会自动尊重 `.gitignore`，但你可能还需要额外的忽略规则。

**最佳实践**：在项目根目录创建一个 `.claudeignore`（如果支持）或者确保 `.gitignore` 覆盖了以下内容：
- `node_modules/`
- `dist/` 或 `build/`
- `.env` (包含密钥的文件)
- `*.log`

### 3.1.2 权限与安全边界
Claude Code 在 Agent 模式下可以执行 shell 命令。为了安全起见：
- **不要在生产服务器上直接运行 Agent 模式**，除非你非常清楚自己在做什么。
- 建议在 Docker 容器或本地开发环境中运行，确保持久化数据有备份。

---

## 3.2 日常开发中的使用模式

我们来看几个最常见的开发场景，以及 Claude Code 在其中的角色。

### 3.2.1 模式 A：作为“结对编程伙伴” (The Pair Programmer)
这是最自然的用法。你和 Claude Code 一起工作，你负责设计和审查，它负责实现细节。

**流程**：
1.  **你**：定义接口结构或写一段伪代码。
2.  **Claude**：补全具体实现。
3.  **你**：指出逻辑漏洞或风格问题。
4.  **Claude**：修正代码。

**适用场景**：编写工具函数、编写样板代码、编写单元测试。

### 3.2.2 模式 B：作为“初级架构师” (The Junior Architect)
当你需要进行模块重构或设计新功能时，Claude Code 可以帮你梳理思路。

**流程**：
1.  **你**：`claude plan "我想把用户认证逻辑从 App.vue 抽离到独立的 composable 中"`。
2.  **Claude**：分析现状，列出需要修改的文件（App.vue, login.ts, store.ts），并提示潜在风险。
3.  **你**：审查计划，确认无误。
4.  **Claude**：`claude "开始执行上述计划"`。

**适用场景**：中等规模的重构、模块拆分、技术栈迁移。

### 3.2.3 模式 C：作为“运维/救火队员” (The Ops/Firefighter)
当系统报错或测试挂掉时，Claude Code 是最好的日志分析器。

**流程**：
1.  **系统**：抛出一大堆 traceback。
2.  **你**：`claude debug` 或直接粘贴错误日志。
3.  **Claude**：指出“第 42 行的变量未定义”，并检查上次 commit 的变动，发现是拼写错误。
4.  **Claude**：提出修复补丁。

---

## 3.3 典型工作流示例

让我们通过三个具体的故事，看看这些模式是如何串联起来的。

### 3.3.1 故事一：测试驱动开发 (TDD) 的新玩法

**传统 TDD**：红（写失败测试） -> 绿（写实现让测试通过） -> 重构。
**Claude TDD**：

1.  **红**：你创建一个测试文件 `user.test.ts`，写下测试用例：
    ```typescript
    it('should calculate discount correctly', () => {
      expect(calcDiscount(100, 'VIP')).toBe(80);
    });
    ```
2.  **Agent**：你运行命令：
    ```bash
    $ claude "实现 calcDiscount 函数，使 user.test.ts 通过"
    ```
3.  **绿**：Claude 读取测试代码，实现函数逻辑，运行测试，直到变绿。
4.  **重构**：你审查代码，发现逻辑太啰嗦，于是说：
    ```bash
    $ claude "重构 calcDiscount，用策略模式优化 switch-case"
    ```

### 3.3.2 故事二：遗留代码的“考古挖掘”

你接手了一个 5 年前的 Python 项目，里面有一个 500 行的 `process_data` 函数，没人敢动。

1.  **Ask**：
    ```bash
    $ claude ask "阅读 process_data 函数，用中文解释它的主要步骤，并画一个流程图"
    ```
    Claude 帮你理清了逻辑，你发现它其实只做了三件事：清洗、计算、入库。

2.  **Plan**：
    ```bash
    $ claude plan "将 process_data 拆分为 clean_data, calc_logic, save_to_db 三个函数，保持原有逻辑不变"
    ```
    Claude 列出拆分方案，你确认没问题。

3.  **Agent**：
    ```bash
    $ claude "执行上述拆分，并确保现有测试（如果有的话）依然通过"
    ```

### 3.3.3 故事三：修复难以复现的 Bug

线上偶尔报 `NullPointerException`，但本地很难复现。

1.  **Ask**：
    ```bash
    $ claude ask "根据这段 Sentry 日志（粘贴日志），分析可能导致空指针的原因"
    ```
    Claude 提示：可能是 `user.profile` 在某些边缘情况下为空。

2.  **Agent (写测试)**：
    ```bash
    $ claude "写一个复现脚本，模拟 user.profile 为空的情况，验证是否会报错"
    ```

3.  **Debug**：
    运行复现脚本，果然报错。
    ```bash
    $ claude "修复这个 Bug，添加空值检查"
    ```

---

## 3.4 效率小贴士

最后，分享几个让 Claude Code 更好用的小技巧：

1.  **使用 Alias (别名)**：
    在你的 shell 配置文件（`.zshrc` 或 `.bashrc`）里添加：
    ```bash
    alias c="claude"
    alias ca="claude ask"
    alias cp="claude plan"
    ```
    这样你就可以用 `c "fix bug"` 快速调用了。

2.  **保持 Commit 粒度**：
    尽量让 Claude Code 做完一个小任务（如修复一个函数）就提交一次 git commit。不要让它一次性改几十个文件，否则 Code Review 会变成噩梦。

3.  **善用 `--print`**：
    如果你只想看它生成的代码，不想让它自动写入文件，可以使用相关参数（视具体版本而定，通常有只输出不执行的选项）。

通过这些工作流的组合，你会发现 Claude Code 不再是一个需要你“费力提问”的工具，而是一个自然融入你指尖的强大插件。
