import re
from pathlib import Path

def remove_subsection_images():
    docs_dir = Path("docs")
    # Directories to process
    subdirs = [
        "00-preface", "10-claude-code", "20-skill", 
        "30-mcp", "40-practices", "90-appendix"
    ]
    
    # Pattern for markdown images: ![alt](url)
    img_pattern = re.compile(r'!\[.*?\]\(.*?\)')
    
    for subdir in subdirs:
        dir_path = docs_dir / subdir
        if not dir_path.exists():
            continue
            
        for file_path in dir_path.glob("*.md"):
            print(f"Processing {file_path}")
            content = file_path.read_text(encoding="utf-8")
            
            # Find all image matches
            matches = list(img_pattern.finditer(content))
            
            if len(matches) <= 1:
                print(f"  - No subsection images found (total images: {len(matches)})")
                continue
            
            print(f"  - Removing {len(matches) - 1} subsection images...")
                
            # We want to keep the FIRST match (Chapter Cover)
            # and remove all SUBSEQUENT matches.
            
            new_content = ""
            last_pos = 0
            
            # Keep the first image
            first_match = matches[0]
            # Content up to the end of the first image
            new_content += content[last_pos:first_match.end()]
            last_pos = first_match.end()
            
            # For remaining matches, replace them with empty string
            for match in matches[1:]:
                # Add text between previous match and current match
                # But we also want to clean up surrounding newlines if the image was on its own line
                
                pre_text = content[last_pos:match.start()]
                new_content += pre_text
                
                # Skip the match (effectively removing it)
                last_pos = match.end()
                
            # Add remaining text
            new_content += content[last_pos:]
            
            # Optional: Clean up multiple empty lines resulting from removal
            # This is a simple heuristic: replace 3+ newlines with 2
            new_content = re.sub(r'\n{3,}', '\n\n', new_content)
            
            # Write back
            file_path.write_text(new_content, encoding="utf-8")

if __name__ == "__main__":
    remove_subsection_images()
