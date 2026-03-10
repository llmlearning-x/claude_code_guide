---
title: 附录 B：示例代码与仓库结构
---

# 附录 B　示例代码与仓库结构说明

![附录：示例代码结构说明](../images/appendix-code-cover.png)

本书的所有示例代码均托管在 GitHub 上。本附录将为你介绍代码仓库的结构，帮助你快速找到所需的参考代码。

> **GitHub 仓库地址**： `https://github.com/your-username/claude-code-guide` (示例)

## B.1 skills 示例目录导读

`examples/skills/` 目录下包含了第 6-8 章介绍的各种 Skill 实现。

```
examples/skills/
├── basic/
│   ├── git-commit/        # [基础] 封装 Git 提交命令
│   └── npm-audit/         # [基础] 封装 npm 安全检查
├── advanced/
│   ├── db-migration/      # [进阶] 数据库迁移脚本封装
│   └── deploy-script/     # [进阶] 包含确认逻辑的部署脚本
└── workflow/
    └── pr-helper/         # [工作流] 自动化 PR 创建与描述生成
```

**如何使用**：
你可以直接将这些目录下的 `CLAUDE.md` 内容复制到你自己的项目中，或者参考其中的 Shell 脚本编写方式。

## B.2 mcp 示例目录导读

`examples/mcp/` 目录下包含了第 9-11 章介绍的 MCP Server 实现。

```
examples/mcp/
├── first-server/          # [入门] "Hello World" 级别的天气查询 Server
│   ├── index.ts
│   └── package.json
├── sqlite-browser/        # [实战] SQLite 数据库浏览器
│   ├── src/
│   │   └── server.ts
│   └── README.md
├── k8s-observer/          # [实战] Kubernetes 只读观察者
│   └── ...
└── legacy-bridge/         # [实战] 连接旧版 SOAP 接口的适配器
    └── ...
```

**如何使用**：
每个子目录都是一个独立的 npm 项目。进入目录后，运行 `npm install && npm run build` 即可构建。然后在 Claude 配置文件中指向构建后的产物。

## B.3 项目实战代码结构

在第 12 章“小型 Web 应用”实战中，我们推荐了如下的项目结构。这种结构非常适合 Claude Code 理解和维护。

```
my-web-app/
├── CLAUDE.md              # [关键] 项目级的 Claude 指南
├── product_requirements.md # [关键] 需求文档
├── src/
│   ├── components/        # UI 组件
│   │   ├── common/        # 通用组件 (Button, Input)
│   │   └── domain/        # 业务组件 (BookCard, UserProfile)
│   ├── hooks/             # 自定义 React Hooks
│   ├── services/          # API 请求封装
│   ├── stores/            # 状态管理 (Zustand)
│   ├── types/             # TypeScript 类型定义
│   └── utils/             # 工具函数
├── tests/                 # 测试文件
└── README.md              # 项目文档
```

**设计要点**：
1.  **模块化**：文件职责单一，方便 Claude 读取和修改。
2.  **类型优先**：`types/` 目录存放核心领域模型，Claude 会优先读取这里来理解业务。
3.  **显式文档**：`product_requirements.md` 和 `CLAUDE.md` 是与 AI 协作的契约。
