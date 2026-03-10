import { fileURLToPath } from 'node:url'
import mermaidPlugin from 'vitepress-plugin-mermaid'

export default {
  title: 'Claude Code 工程实践（预览版）',
  description: 'Claude Code + Skill + MCP 工程实践书籍在线阅读版',
  srcDir: '../docs',
  outDir: './dist',
  lang: 'zh-CN',
  lastUpdated: true,
  themeConfig: {
    nav: [
      { text: '主页', link: '/' },
      { text: '前言', link: '/00-preface/' },
      { text: 'Claude Code 基础', link: '/10-claude-code/intro' },
      { text: 'Skill', link: '/20-skill/intro' },
      { text: 'MCP', link: '/30-mcp/intro' },
      { text: '实战', link: '/40-practices/web-app' },
      { text: '附录', link: '/90-appendix/prompt-index' }
    ],
    outline: {
      // 显示二级、三级标题到 “On this page”
      level: [2, 3]
    },
    sidebar: [
      {
        text: '前言',
        items: [
          { text: '前言', link: '/00-preface/' }
        ]
      },
      {
        text: '第 I 部分　Claude Code 基础与工作流',
        items: [
          { text: '第 1 章　Claude Code 概览', link: '/10-claude-code/intro' },
          { text: '第 2 章　模式体系', link: '/10-claude-code/modes' },
          { text: '第 3 章　日常工作流', link: '/10-claude-code/workflow' },
          { text: '第 4 章　工程级 Prompt 设计', link: '/10-claude-code/prompts' }
        ]
      },
      {
        text: '第 II 部分　Skill：把任务变成能力',
        items: [
          { text: '第 5 章　Skill 入门', link: '/20-skill/intro' },
          { text: '第 6 章　Skill 设计模式', link: '/20-skill/design-patterns' },
          { text: '第 7 章　团队级 Skill 体系', link: '/20-skill/team-system' }
        ]
      },
      {
        text: '第 III 部分　MCP：连接外部世界',
        items: [
          { text: '第 8 章　MCP 概念与设计思想', link: '/30-mcp/intro' },
          { text: '第 9 章　第一个 MCP 服务', link: '/30-mcp/first-service' },
          { text: '第 10 章　MCP 深度集成', link: '/30-mcp/deep-integration' },
          { text: '第 11 章　MCP 安全与部署', link: '/30-mcp/security' }
        ]
      },
      {
        text: '第 IV 部分　项目与团队实战',
        items: [
          { text: '第 12 章　小型 Web 应用', link: '/40-practices/web-app' },
          { text: '第 13 章　后端 API 服务与运维助手', link: '/40-practices/backend-ops' },
          { text: '实战指南：阿里云 ECS 部署流程', link: '/40-practices/deployment-ecs' },
          { text: '第 14 章　遗留系统改造', link: '/40-practices/legacy-refactor' },
          { text: '第 15 章　在团队中落地 Claude Code', link: '/40-practices/team-adoption' }
        ]
      },
      {
        text: '第 V 部分　附录',
        items: [
          { text: '附录 A　Prompt 模板索引', link: '/90-appendix/prompt-index' },
          { text: '附录 B　示例代码与仓库结构', link: '/90-appendix/code-structure' },
          { text: '附录 C　术语表', link: '/90-appendix/glossary' },
          { text: '附录 D　常见问题与排错指南', link: '/90-appendix/faq' }
        ]
      }
    ],
    search: {
      provider: 'local'
    }
  },
  markdown: {
    config: (md) => {
      md.use(mermaidPlugin)
    }
  },
  vite: {
    resolve: {
      alias: [
        {
          find: /^vue$/,
          replacement: fileURLToPath(
            new URL('../node_modules/vue/dist/vue.runtime.esm-bundler.js', import.meta.url)
          )
        },
        {
          find: /^vue\/server-renderer$/,
          replacement: fileURLToPath(
            new URL('../node_modules/vue/server-renderer/index.mjs', import.meta.url)
          )
        }
      ]
    }
  }
}
