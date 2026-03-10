import { h } from 'vue'
import DefaultTheme from 'vitepress/theme'
import './custom.css'
import ScrollToTopBottom from './components/ScrollToTopBottom.vue'

// 由 vitepress-plugin-mermaid 提供的 Mermaid 组件
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import Mermaid from 'vitepress-plugin-mermaid/Mermaid.vue'

export default {
  ...DefaultTheme,
  Layout: () => {
    return h(DefaultTheme.Layout, null, {
      'layout-bottom': () => h(ScrollToTopBottom)
    })
  },
  enhanceApp({ app }) {
    app.component('Mermaid', Mermaid)
  }
}
