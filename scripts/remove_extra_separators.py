import re
from pathlib import Path

def remove_extra_separators():
    docs_dir = Path("docs")
    
    # Iterate over all markdown files recursively
    for file_path in docs_dir.rglob("*.md"):
        print(f"Processing {file_path}")
        content = file_path.read_text(encoding="utf-8")
        
        # Split frontmatter from body
        # Frontmatter starts with --- on the first line
        if content.startswith("---\n"):
            parts = content.split("---\n", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                body = parts[2]
                
                # In the body, replace "---" lines that are likely separators
                # We look for --- surrounded by newlines
                # Regex: newline, optional whitespace, ---, optional whitespace, newline
                
                # Replace "\n---\n" with "\n"
                # But we need to handle potential multiple newlines
                
                new_body = re.sub(r'\n\s*---\s*\n', '\n\n', body)
                
                # Reassemble
                new_content = f"---\n{frontmatter}---\n{new_body}"
                
                if new_content != content:
                    print(f"  - Removed separators in {file_path.name}")
                    file_path.write_text(new_content, encoding="utf-8")
                else:
                    print(f"  - No changes needed for {file_path.name}")
            else:
                print(f"  - Warning: Malformed frontmatter in {file_path.name}")
        else:
            # No frontmatter, process whole file
            new_content = re.sub(r'\n\s*---\s*\n', '\n\n', content)
            if new_content != content:
                print(f"  - Removed separators in {file_path.name}")
                file_path.write_text(new_content, encoding="utf-8")

if __name__ == "__main__":
    remove_extra_separators()
