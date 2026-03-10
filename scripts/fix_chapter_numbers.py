import re
from pathlib import Path

# Mapping of file path to chapter number
CHAPTER_MAP = {
    "10-claude-code/intro.md": 1,
    "10-claude-code/modes.md": 2,
    "10-claude-code/workflow.md": 3,
    "10-claude-code/prompts.md": 4,
    "20-skill/intro.md": 5,
    "20-skill/design-patterns.md": 6,
    "20-skill/team-system.md": 7,
    "30-mcp/intro.md": 8,
    "30-mcp/first-service.md": 9,
    "30-mcp/deep-integration.md": 10,
    "30-mcp/security.md": 11,
    "40-practices/web-app.md": 12,
    "40-practices/backend-ops.md": 13,
    "40-practices/legacy-refactor.md": 14,
    "40-practices/team-adoption.md": 15,
}

def fix_chapter_numbers():
    docs_dir = Path("docs")
    
    for rel_path, chapter_num in CHAPTER_MAP.items():
        file_path = docs_dir / rel_path
        if not file_path.exists():
            print(f"Warning: {file_path} not found")
            continue
            
        print(f"Processing Chapter {chapter_num}: {rel_path}")
        content = file_path.read_text(encoding="utf-8")
        original_content = content
        
        # Replace headers like "## X.1 Title"
        def replace_header_x(match):
            hashes = match.group(1)
            sub_num = match.group(2)
            return f"{hashes} {chapter_num}.{sub_num}"
            
        content = re.sub(r'^(#+)\s+X\.(\d+)', replace_header_x, content, flags=re.MULTILINE)
        
        # Replace Figure refs like "图 X-1"
        # Using lambda to avoid backreference ambiguity
        content = re.sub(r'图 X[‑-](\d+)', lambda m: f'图 {chapter_num}-{m.group(1)}', content)
        content = re.sub(r'Figure X[‑-](\d+)', lambda m: f'Figure {chapter_num}-{m.group(1)}', content)
        
        # Replace text refs like "X.2"
        # Be careful not to replace things that aren't section numbers
        # We look for "X." followed by a digit, preceded by whitespace or start of line
        def replace_text_ref(match):
            prefix = match.group(1)
            sub_num = match.group(2)
            return f"{prefix}{chapter_num}.{sub_num}"
            
        content = re.sub(r'(^|\s)X\.(\d+)', replace_text_ref, content)

        if content != original_content:
            print(f"  - Updated content in {rel_path}")
            file_path.write_text(content, encoding="utf-8")
        else:
            print(f"  - No changes needed for {rel_path}")

if __name__ == "__main__":
    fix_chapter_numbers()
