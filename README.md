# Claude Code Guide

This repository contains the source code for the "Claude Code Engineering Practice" book, built with VitePress.

## Project Structure

- `docs/`: Markdown source files for the documentation.
- `site/`: VitePress configuration and theme customization.
- `scripts/`: Utility scripts for build and maintenance.

## Development

To run the documentation site locally:

```bash
cd site
npm install
npm run docs:dev
```

## Deployment

The site is deployed to [GitHub Pages](https://llmlearning-x.github.io/claude_code_guide/) (assuming GitHub Pages is enabled) or other hosting services.

See `docs/40-practices/deployment-ecs.md` for ECS deployment instructions.
