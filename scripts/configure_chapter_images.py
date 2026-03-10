import os
import re
import shutil
from pathlib import Path

# Mapping of file path to image details
# Key: relative path from docs/
CHAPTER_IMAGES = {
    # 00-preface
    "00-preface/index.md": {
        "image": "preface-cover.png",
        "alt": "前言：工程世界的复杂性与挑战",
        "title": "前言"
    },
    # 10-claude-code
    "10-claude-code/intro.md": {
        "image": "cc-intro-cover.png", # Existing
        "alt": "Claude Code 概览：人机协作的新范式",
        "title": "第 1 章　Claude Code 概览"
    },
    "10-claude-code/modes.md": {
        "image": "cc-modes-cover.png",
        "alt": "Claude Code 模式体系：Ask/Plan/Agent/Debug",
        "title": "第 2 章　模式体系"
    },
    "10-claude-code/workflow.md": {
        "image": "cc-workflow-cover.png",
        "alt": "日常工作流：从需求分析到代码交付",
        "title": "第 3 章　日常工作流"
    },
    "10-claude-code/prompts.md": {
        "image": "cc-prompts-cover.png",
        "alt": "工程级 Prompt 设计：结构化与复用",
        "title": "第 4 章　工程级 Prompt 设计"
    },
    # 20-skill
    "20-skill/intro.md": {
        "image": "skill-intro-cover.png", # Existing
        "alt": "Skill 入门：构建你的工程工具箱",
        "title": "第 5 章　Skill 入门"
    },
    "20-skill/design-patterns.md": {
        "image": "skill-patterns-cover.png",
        "alt": "Skill 设计模式：常见架构与最佳实践",
        "title": "第 6 章　Skill 设计模式"
    },
    "20-skill/team-system.md": {
        "image": "skill-team-cover.png",
        "alt": "团队级 Skill 体系：共享与协作",
        "title": "第 7 章　团队级 Skill 体系"
    },
    # 30-mcp
    "30-mcp/intro.md": {
        "image": "mcp-intro-cover.png",
        "alt": "MCP 概念：连接 AI 与外部世界的桥梁",
        "title": "第 8 章　MCP 概念与设计思想"
    },
    "30-mcp/first-service.md": {
        "image": "mcp-first-service-cover.png",
        "alt": "第一个 MCP 服务：从零开始构建",
        "title": "第 9 章　第一个 MCP 服务"
    },
    "30-mcp/deep-integration.md": {
        "image": "mcp-deep-integration-cover.png",
        "alt": "MCP 深度集成：复杂场景下的应用",
        "title": "第 10 章　MCP 深度集成"
    },
    "30-mcp/security.md": {
        "image": "mcp-security-cover.png",
        "alt": "MCP 安全与部署：生产环境的最佳实践",
        "title": "第 11 章　MCP 安全与部署"
    },
    # 40-practices
    "40-practices/web-app.md": {
        "image": "practices-web-app-cover.png",
        "alt": "实战：小型 Web 应用开发全流程",
        "title": "第 12 章　小型 Web 应用"
    },
    "40-practices/backend-ops.md": {
        "image": "practices-backend-ops-cover.png",
        "alt": "实战：后端 API 服务与自动化运维",
        "title": "第 13 章　后端 API 服务与运维助手"
    },
    "40-practices/legacy-refactor.md": {
        "image": "practices-legacy-cover.png",
        "alt": "实战：遗留系统重构与现代化",
        "title": "第 14 章　遗留系统改造"
    },
    "40-practices/team-adoption.md": {
        "image": "practices-team-adoption-cover.png",
        "alt": "团队落地：文化建设与流程规范",
        "title": "第 15 章　在团队中落地 Claude Code"
    },
    # 90-appendix
    "90-appendix/prompt-index.md": {
        "image": "appendix-prompt-cover.png",
        "alt": "附录：Prompt 模板索引与参考",
        "title": "附录 A　Prompt 模板索引"
    },
    "90-appendix/code-structure.md": {
        "image": "appendix-code-cover.png",
        "alt": "附录：示例代码结构说明",
        "title": "附录 B　示例代码与仓库结构"
    },
    "90-appendix/glossary.md": {
        "image": "appendix-glossary-cover.png",
        "alt": "附录：术语表与概念解释",
        "title": "附录 C　术语表"
    },
    "90-appendix/faq.md": {
        "image": "appendix-faq-cover.png",
        "alt": "附录：常见问题解答与排错指南",
        "title": "附录 D　常见问题与排错指南"
    }
}

def setup_images():
    docs_dir = Path("docs")
    images_dir = docs_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Source for placeholders
    source_img = images_dir / "cc-intro-cover.png"
    if not source_img.exists():
        # Fallback if specific source doesn't exist, try to find any png
        pngs = list(images_dir.glob("*.png"))
        if pngs:
            source_img = pngs[0]
        else:
            print("Error: No source image found to create placeholders.")
            return

    # Create placeholders
    for info in CHAPTER_IMAGES.values():
        img_path = images_dir / info["image"]
        if not img_path.exists():
            print(f"Creating placeholder: {img_path.name}")
            shutil.copy(source_img, img_path)

def update_markdown_files():
    docs_dir = Path("docs")
    
    for rel_path, info in CHAPTER_IMAGES.items():
        file_path = docs_dir / rel_path
        if not file_path.exists():
            print(f"Warning: File {file_path} not found.")
            continue
            
        content = file_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        # Check if image already exists near the top (after H1)
        # We look for H1, then check if the next few lines contain an image
        
        h1_index = -1
        for i, line in enumerate(lines):
            if line.startswith("# "):
                h1_index = i
                break
        
        if h1_index == -1:
            print(f"Warning: No H1 title found in {rel_path}")
            continue
            
        # Check if there is already an image in the next 5 lines
        has_image = False
        for i in range(h1_index + 1, min(h1_index + 10, len(lines))):
            if lines[i].strip().startswith("!["):
                has_image = True
                break
        
        if not has_image:
            print(f"Inserting image into {rel_path}")
            # Insert image after H1 with spacing
            image_markdown = f"\n![{info['alt']}](../images/{info['image']})\n"
            lines.insert(h1_index + 1, image_markdown)
            
            file_path.write_text("\n".join(lines), encoding="utf-8")
        else:
            print(f"Image already exists in {rel_path}")

def generate_manifest():
    manifest_path = Path("docs/chapter_images.md")
    content = ["# 章节图片清单", "", "| 章节 | 文件名 | 说明 | 来源 |", "| --- | --- | --- | --- |"]
    
    for rel_path, info in CHAPTER_IMAGES.items():
        chapter = info["title"]
        filename = info["image"]
        alt = info["alt"]
        source = "自制 / Placeholder"
        content.append(f"| {chapter} | `{filename}` | {alt} | {source} |")
    
    manifest_path.write_text("\n".join(content), encoding="utf-8")
    print(f"Manifest generated at {manifest_path}")

if __name__ == "__main__":
    setup_images()
    update_markdown_files()
    generate_manifest()
