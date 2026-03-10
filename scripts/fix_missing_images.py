import os
import re
from pathlib import Path
import shutil

def main():
    docs_dir = Path("docs")
    images_dir = docs_dir / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Source image to copy for placeholders
    source_img = images_dir / "cc-intro-cover.png"
    if not source_img.exists():
        print(f"Error: Source image {source_img} not found.")
        # Try to find any png file
        pngs = list(images_dir.glob("*.png"))
        if pngs:
            source_img = pngs[0]
            print(f"Using {source_img} as source.")
        else:
            print("No png images found to use as placeholder source.")
            return

    # Regex to find markdown images: ![alt](url)
    img_re = re.compile(r'!\[.*?\]\((.*?)\)')
    
    missing_count = 0
    
    for md_file in docs_dir.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
            continue
            
        matches = img_re.findall(content)
        
        for url in matches:
            # Resolve URL relative to md_file
            if url.startswith("http") or url.startswith("//"):
                continue
                
            # Remove query params or hash
            clean_url = url.split('?')[0].split('#')[0]
            
            # Resolve path
            # Assuming relative paths like ../images/foo.png or ./foo.png
            try:
                img_path = (md_file.parent / clean_url).resolve()
            except Exception as e:
                print(f"Error resolving {url} in {md_file}: {e}")
                continue
                
            if not img_path.exists():
                print(f"Missing: {img_path}")
                
                # Create directory if needed
                img_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy placeholder
                try:
                    shutil.copy(source_img, img_path)
                    print(f"Created placeholder: {img_path.name}")
                    missing_count += 1
                except Exception as e:
                    print(f"Failed to create placeholder for {img_path}: {e}")

    print(f"Fixed {missing_count} missing images.")

if __name__ == "__main__":
    main()
