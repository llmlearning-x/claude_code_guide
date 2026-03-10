import fs from 'node:fs'
import path from 'node:path'

const __dirname = path.dirname(new URL(import.meta.url).pathname)
const rootDir = path.resolve(__dirname, '..')
const buildDir = path.join(rootDir, 'build')

const htmlRoot = 'html/index.html'
const pdfPath = 'pdf/claude-code-engineering-v0.1.0.pdf'

const bookConfigPath = path.join(rootDir, 'book.config.json')
const bookConfig = JSON.parse(fs.readFileSync(bookConfigPath, 'utf-8'))

const manifest = {
  id: bookConfig.id,
  title: bookConfig.title,
  subtitle: bookConfig.subtitle,
  version: bookConfig.version,
  language: bookConfig.language,
  abstract: bookConfig.abstract,
  authors: bookConfig.authors,
  keywords: bookConfig.keywords,
  license: bookConfig.license,
  homepage: bookConfig.homepage,
  buildTime: new Date().toISOString(),
  files: {
    htmlRoot,
    pdf: pdfPath
  }
}

if (!fs.existsSync(buildDir)) {
  fs.mkdirSync(buildDir, { recursive: true })
}

fs.writeFileSync(
  path.join(buildDir, 'manifest.json'),
  JSON.stringify(manifest, null, 2),
  'utf-8'
)

console.log('manifest.json generated at build/manifest.json')

