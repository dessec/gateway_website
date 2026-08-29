import re
from pathlib import Path

files_to_update = [Path("index.html")] + list(Path("pages").glob("*.html"))

# We want to replace the navbar medallion image specifically inside <nav>...</nav>
def update_nav_medallion(content):
    # Find <nav ...> ... </nav>
    nav_match = re.search(r'(<nav\b[^>]*>.*?</nav>)', content, re.DOTALL)
    if not nav_match:
        return content
    
    nav_content = nav_match.group(1)
    # replace class="h-11 w-auto... with class="h-16 w-auto... in nav
    updated_nav = re.sub(
        r'class="h-11 w-auto object-contain drop-shadow-md group-hover:scale-105 transition-transform duration-300"',
        r'class="h-16 w-auto object-contain drop-shadow-md group-hover:scale-105 transition-transform duration-300"',
        nav_content
    )
    return content[:nav_match.start(1)] + updated_nav + content[nav_match.end(1):]

for file_path in files_to_update:
    content = file_path.read_text(encoding="utf-8")
    updated = update_nav_medallion(content)
    if updated != content:
        file_path.write_text(updated, encoding="utf-8")
        print(f"Updated navbar medallion in {file_path}")
    else:
        print(f"No changes in {file_path}")
