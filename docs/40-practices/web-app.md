---
title: 实战一：小型 Web 应用
---

# 第 12 章　实战一：小型 Web 应用从 0 到 1

![实战：小型 Web 应用开发全流程](../images/practices-web-app-cover.png)

在这个章节中，我们将通过一个真实的案例——开发一个**个人图书追踪器 (Personal Book Tracker)**，来完整演示如何利用 Claude Code 从零开始构建一个现代 Web 应用。

这个过程不再是简单的“写代码”，而是你作为架构师，指挥 Claude Code 完成从需求分析到上线的全过程。

## 12.1 需求与领域建模

在开始写代码之前，我们需要明确“做什么”。对于 Claude 来说，清晰的需求文档就是最好的 Prompt。

### 12.1.1 编写 `product_requirements.md`

不要直接对 Claude 说“做一个图书管理系统”。相反，你应该先创建一个 `product_requirements.md` 文件，详细描述你的构想。

```markdown
# Personal Book Tracker 需求文档

## 核心功能
1.  **用户认证**：简单的本地模拟认证或 OAuth。
2.  **图书管理**：
    -   添加图书（ISBN 自动查询，使用 Google Books API）。
    -   列表展示（按阅读状态：想读、在读、已读）。
    -   评分与笔记。
3.  **数据统计**：
    -   年度阅读量图表。
    -   阅读偏好分析（基于标签）。

## 技术栈
-   前端：React + TypeScript + Vite + Tailwind CSS
-   状态管理：Zustand
-   数据持久化：LocalStorage (为了简化演示，不涉及后端数据库)
```

有了这个文件，你可以对 Claude 说：
> “Claude，请读取 `product_requirements.md`，并根据它为我生成项目的初始文件结构建议。”

### 12.1.2 领域模型确认

Claude 会根据需求文档，分析出核心的数据结构：

```typescript
// Claude 建议的类型定义
interface Book {
  id: string;
  isbn: string;
  title: string;
  author: string;
  coverUrl: string;
  status: 'reading' | 'completed' | 'wishlist';
  rating?: number;
  notes?: string;
  addedAt: Date;
}
```

这一步非常关键。如果模型设计有误，后续的代码都会歪。请务必在这个阶段与 Claude 确认清楚。

## 12.2 搭建项目骨架

确认了需求和模型后，我们开始动工。

### 12.2.1 初始化工程

直接在终端运行 Claude：

```bash
$ claude
> 请使用 Vite 创建一个 React + TypeScript 项目，命名为 book-tracker。
> 安装 Tailwind CSS 并配置好基础样式。
> 安装 lucide-react 作为图标库。
```

Claude 会自动执行 `npm create vite@latest`，并帮你修改 `tailwind.config.js`。你只需要看着终端里的进度条飞快走过。

### 12.2.2 建立 `CLAUDE.md`

为了确保 Claude 在后续开发中遵循我们的规范，我们在项目根目录创建 `CLAUDE.md`：

```markdown
# Claude Code Guide for Book Tracker

## Commands
- Run: `npm run dev`
- Build: `npm run build`
- Test: `npm run test`

## Code Style
- Use Functional Components with Hooks.
- Use TypeScript interfaces for props.
- Use Tailwind CSS for styling (no CSS modules).
- Store state in Zustand stores (src/stores).
- Components go in `src/components`, pages in `src/pages`.
```

这个文件就像是给 Claude 的“员工手册”。每次对话开始时，Claude 都会先看一眼这个文件，从而保证生成的代码风格一致。

## 12.3 关键功能开发

现在，我们进入核心开发阶段。

### 12.3.1 开发“添加图书”功能 (集成外部 API)

这是最复杂的部分，涉及 API 调用。

> **User**: “我要实现添加图书的功能。用户输入 ISBN，应用调用 Google Books API 获取信息。请在 `src/services/bookApi.ts` 中实现 API 调用，并在 `src/components/AddBookForm.tsx` 中实现 UI。”

Claude 会：
1.  搜索 Google Books API 的文档（或利用其内置知识）。
2.  编写 `fetchBookByISBN` 函数，处理异步请求和错误。
3.  编写表单组件，包含输入框和“搜索”按钮。
4.  **自动处理边缘情况**：比如“未找到图书”或“网络错误”的提示。

### 12.3.2 状态管理与数据持久化

> **User**: “现在创建 `useBookStore`，使用 Zustand 管理图书列表，并实现 `persist` 中间件把数据存到 LocalStorage。”

Claude 会生成一个类型安全的 Store，包含 `addBook`, `updateBook`, `removeBook` 等 Actions。

### 12.3.3 数据可视化

> **User**: “在首页增加一个统计卡片，显示‘今年已读’的数量。如果数量超过 10 本，显示一个‘太棒了’的徽章。”

Claude 能迅速理解这种业务逻辑，并修改对应的组件。

## 12.4 上线前检查与回顾

功能开发完成后，不要急着庆祝。

### 12.4.1 自动化测试

> **User**: “为 `bookApi.ts` 编写单元测试，模拟 API 响应。为 `AddBookForm` 编写组件测试，确保输入为空时按钮禁用。”

Claude 会使用 Vitest 或 Jest 编写测试用例。你会发现，AI 写测试代码的质量通常很高，因为它能覆盖到你容易忽略的边界条件。

### 12.4.2 生成文档

最后，让 Claude 帮你写 `README.md`：

> **User**: “根据当前项目代码，生成一个精美的 README。包含项目简介、安装步骤、功能列表和截图占位符。”

### 小结

通过这个案例，你体验了 Claude Code 的完整工作流：
1.  **Read**: 读取需求文档。
2.  **Plan**: 设计数据结构。
3.  **Act**: 生成代码、执行命令。
4.  **Review**: 编写测试、补充文档。

在下一章，我们将离开浏览器，深入后端与运维的世界。
