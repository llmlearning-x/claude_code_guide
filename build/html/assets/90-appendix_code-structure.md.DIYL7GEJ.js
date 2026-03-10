import{_ as a,o as n,c as p,ai as e}from"./chunks/framework.BIXs0jTs.js";const l="/assets/preface-cover.Balx8Fq4.png",h=JSON.parse('{"title":"附录 B：示例代码与仓库结构","description":"","frontmatter":{"title":"附录 B：示例代码与仓库结构"},"headers":[],"relativePath":"90-appendix/code-structure.md","filePath":"90-appendix/code-structure.md","lastUpdated":null}'),t={name:"90-appendix/code-structure.md"};function i(c,s,o,r,d,u){return n(),p("div",null,[...s[0]||(s[0]=[e('<h1 id="附录-b-示例代码与仓库结构说明" tabindex="-1">附录 B　示例代码与仓库结构说明 <a class="header-anchor" href="#附录-b-示例代码与仓库结构说明" aria-label="Permalink to &quot;附录 B　示例代码与仓库结构说明&quot;">​</a></h1><p><img src="'+l+`" alt="附录：示例代码结构说明"></p><p>本书的所有示例代码均托管在 GitHub 上。本附录将为你介绍代码仓库的结构，帮助你快速找到所需的参考代码。</p><blockquote><p><strong>GitHub 仓库地址</strong>： <code>https://github.com/your-username/claude-code-guide</code> (示例)</p></blockquote><h2 id="b-1-skills-示例目录导读" tabindex="-1">B.1 skills 示例目录导读 <a class="header-anchor" href="#b-1-skills-示例目录导读" aria-label="Permalink to &quot;B.1 skills 示例目录导读&quot;">​</a></h2><p><code>examples/skills/</code> 目录下包含了第 6-8 章介绍的各种 Skill 实现。</p><div class="language- vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang"></span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>examples/skills/</span></span>
<span class="line"><span>├── basic/</span></span>
<span class="line"><span>│   ├── git-commit/        # [基础] 封装 Git 提交命令</span></span>
<span class="line"><span>│   └── npm-audit/         # [基础] 封装 npm 安全检查</span></span>
<span class="line"><span>├── advanced/</span></span>
<span class="line"><span>│   ├── db-migration/      # [进阶] 数据库迁移脚本封装</span></span>
<span class="line"><span>│   └── deploy-script/     # [进阶] 包含确认逻辑的部署脚本</span></span>
<span class="line"><span>└── workflow/</span></span>
<span class="line"><span>    └── pr-helper/         # [工作流] 自动化 PR 创建与描述生成</span></span></code></pre></div><p><strong>如何使用</strong>： 你可以直接将这些目录下的 <code>CLAUDE.md</code> 内容复制到你自己的项目中，或者参考其中的 Shell 脚本编写方式。</p><h2 id="b-2-mcp-示例目录导读" tabindex="-1">B.2 mcp 示例目录导读 <a class="header-anchor" href="#b-2-mcp-示例目录导读" aria-label="Permalink to &quot;B.2 mcp 示例目录导读&quot;">​</a></h2><p><code>examples/mcp/</code> 目录下包含了第 9-11 章介绍的 MCP Server 实现。</p><div class="language- vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang"></span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>examples/mcp/</span></span>
<span class="line"><span>├── first-server/          # [入门] &quot;Hello World&quot; 级别的天气查询 Server</span></span>
<span class="line"><span>│   ├── index.ts</span></span>
<span class="line"><span>│   └── package.json</span></span>
<span class="line"><span>├── sqlite-browser/        # [实战] SQLite 数据库浏览器</span></span>
<span class="line"><span>│   ├── src/</span></span>
<span class="line"><span>│   │   └── server.ts</span></span>
<span class="line"><span>│   └── README.md</span></span>
<span class="line"><span>├── k8s-observer/          # [实战] Kubernetes 只读观察者</span></span>
<span class="line"><span>│   └── ...</span></span>
<span class="line"><span>└── legacy-bridge/         # [实战] 连接旧版 SOAP 接口的适配器</span></span>
<span class="line"><span>    └── ...</span></span></code></pre></div><p><strong>如何使用</strong>： 每个子目录都是一个独立的 npm 项目。进入目录后，运行 <code>npm install &amp;&amp; npm run build</code> 即可构建。然后在 Claude 配置文件中指向构建后的产物。</p><h2 id="b-3-项目实战代码结构" tabindex="-1">B.3 项目实战代码结构 <a class="header-anchor" href="#b-3-项目实战代码结构" aria-label="Permalink to &quot;B.3 项目实战代码结构&quot;">​</a></h2><p>在第 12 章“小型 Web 应用”实战中，我们推荐了如下的项目结构。这种结构非常适合 Claude Code 理解和维护。</p><div class="language- vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang"></span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>my-web-app/</span></span>
<span class="line"><span>├── CLAUDE.md              # [关键] 项目级的 Claude 指南</span></span>
<span class="line"><span>├── product_requirements.md # [关键] 需求文档</span></span>
<span class="line"><span>├── src/</span></span>
<span class="line"><span>│   ├── components/        # UI 组件</span></span>
<span class="line"><span>│   │   ├── common/        # 通用组件 (Button, Input)</span></span>
<span class="line"><span>│   │   └── domain/        # 业务组件 (BookCard, UserProfile)</span></span>
<span class="line"><span>│   ├── hooks/             # 自定义 React Hooks</span></span>
<span class="line"><span>│   ├── services/          # API 请求封装</span></span>
<span class="line"><span>│   ├── stores/            # 状态管理 (Zustand)</span></span>
<span class="line"><span>│   ├── types/             # TypeScript 类型定义</span></span>
<span class="line"><span>│   └── utils/             # 工具函数</span></span>
<span class="line"><span>├── tests/                 # 测试文件</span></span>
<span class="line"><span>└── README.md              # 项目文档</span></span></code></pre></div><p><strong>设计要点</strong>：</p><ol><li><strong>模块化</strong>：文件职责单一，方便 Claude 读取和修改。</li><li><strong>类型优先</strong>：<code>types/</code> 目录存放核心领域模型，Claude 会优先读取这里来理解业务。</li><li><strong>显式文档</strong>：<code>product_requirements.md</code> 和 <code>CLAUDE.md</code> 是与 AI 协作的契约。</li></ol>`,17)])])}const b=a(t,[["render",i]]);export{h as __pageData,b as default};
