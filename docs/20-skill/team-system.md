---
title: 团队级 Skill 体系
---

# 第 7 章　团队级 Skill 体系：共享与协作

![团队级 Skill 体系：共享与协作](../images/skill-team-cover.png)

如果说个人 Skill 是开发者的“私人瑞士军刀”，那么团队级 Skill 体系就是整个组织的“中央军火库”。

当一个团队有 10 人、50 人甚至 100 人在使用 Claude Code 时，我们面临的挑战就不再是如何写好一个 Prompt，而是：
- 如何让新人一入职就拥有资深员工积累的 Skill？
- 如何防止每个人都写一遍 `generate_sql`，导致出现 10 个不同版本？
- 如何统一管理和更新这些 Skill？

本章将探讨如何构建一个**可扩展、可维护的团队级 Skill 体系**。

## 7.1 从“我的 Skill”到“我们的 Skill”

### 7.1.1 孤岛现象
在没有统一管理的情况下，很容易出现“Prompt 孤岛”：
- Alice 写了一个很棒的 `review_pr` Skill，但只有她自己知道。
- Bob 刚入职，不知道怎么用 Claude 写单测，自己瞎琢磨了一套效果很差的 Prompt。
- Charlie 发现 Alice 的 Skill 有个 Bug，修复了但没告诉 Alice。

### 7.1.2 共享的价值
建立团队级 Skill 库的核心价值在于：
1.  **能力复用**：一次编写，全员受益。
2.  **规范落地**：通过 Skill 强制推行代码规范（如 Commit 格式、命名风格）。
3.  **知识沉淀**：将团队的最佳实践固化为可执行的代码（Skill），而不是躺在 Wiki 里的死文档。

---

## 7.2 管理 Skill 仓库 (GitOps)

最简单的管理方式是使用 Git 仓库。

### 7.2.1 仓库结构推荐
建议创建一个名为 `claude-skills` 或 `engineering-prompts` 的独立仓库。

```text
claude-skills/
├── README.md           # 索引与安装指南
├── skills/             # 核心 Skill 目录
│   ├── git/
│   │   ├── commit-msg.json
│   │   └── pr-desc.json
│   ├── code/
│   │   ├── refactor.json
│   │   └── unit-test.json
│   └── ops/
│       └── k8s-logs.json
├── configs/            # 推荐的 .clauderc 配置
│   └── recommended.json
└── docs/               # 开发文档
```

### 7.2.2 分发机制
如何让每个人的 Claude Code 都能加载这些 Skill？

**方案 A：Git Submodule / Clone（推荐）**
每个开发者在本地机器上 clone 这个仓库，并在自己的 Claude Code 配置中指向该目录。

**方案 B：MCP 服务分发**
建立一个内部的 MCP Server，专门负责通过网络下发 Skill。当 Skill 更新时，服务端更新即可，客户端无感知。这是更高级的玩法（将在第 III 部分详细介绍）。

---

## 7.3 版本控制与发布

Skill 也是代码，应该遵循软件工程的版本管理原则。

### 7.3.1 语义化版本
给 Skill 库打 Tag，例如 `v1.0.0`。
- **Major**：Prompt 逻辑大改，接口不兼容（参数变了）。
- **Minor**：增加了新 Skill，或优化了现有 Skill 的效果。
- **Patch**：修复了 Prompt 中的错别字或微调语气。

### 7.3.2 变更日志 (Changelog)
在 `CHANGELOG.md` 中记录：
> **v1.2.0**
> - 新增 `java_doc_gen` Skill。
> - 优化 `commit_msg`：现在支持 Emoji 前缀了。
> - 修复 `sql_query` 在多表 Join 时的幻觉问题。

---

## 7.4 治理：谁来批准一个 Skill？

不要让 Skill 库变成垃圾场。需要引入 **Skill Review** 机制。

### 7.4.1 提交标准
提交一个新的 Skill 到团队库时，必须包含：
1.  **接口定义**：清晰的输入输出描述。
2.  **测试用例**：至少 3 个“输入-输出”样本，证明它是有效的。
3.  **适用范围**：说明在什么情况下使用（如“仅适用于 Python 项目”）。

### 7.4.2 维护者 (Maintainers)
指定 1-2 位“AI 效能工程师”或资深开发者作为维护者。他们的职责是：
- Review 同事提交的 Skill PR。
- 定期清理过时或低频使用的 Skill。
- 监控 Skill 的使用效果（通过收集反馈）。

### 7.4.3 风格指南
制定一份《Prompt 编写指南》，统一团队的 Prompt 风格：
- 统一称呼（如“你是一个资深工程师”）。
- 统一输出格式（如“优先使用 Markdown 表格”）。
- 统一语言（中文/英文）。

---

## 7.5 小结

团队级 Skill 体系的建设，标志着一个团队从“尝鲜 AI”走向了“AI 工程化”。

- 用 **Git 仓库** 统一管理 Skill。
- 用 **版本控制** 追踪变更。
- 用 **Review 机制** 保证质量。

当你的团队拥有了一套成熟的 Skill 体系，新入职的员工只需 `git clone` 一下，就能立刻获得全团队积累多年的智慧加持。这就是 AI 时代的“站在巨人的肩膀上”。

至此，我们已经完成了关于 Skill 的全部内容。在接下来的**第 III 部分**，我们将跨越 Claude Code 的边界，通过 **MCP (Model Context Protocol)** 去连接更广阔的外部世界——数据库、Jira、Slack 以及生产环境。
