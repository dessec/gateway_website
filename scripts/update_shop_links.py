import re
from pathlib import Path

# 1. Update index.html
index_file = Path("index.html")
if index_file.exists():
    content = index_file.read_text(encoding="utf-8")
    # Replace navbar link
    content = re.sub(r'<a href="#brands" class="nav-link([^"]*)">Shop</a>', r'<a href="pages/shop.html" class="nav-link\1">Shop</a>', content)
    # Footer link
    content = re.sub(r'<li><a href="#brands" class="([^"]*)">Shop</a></li>', r'<li><a href="pages/shop.html" class="\1">Shop</a></li>', content)
    index_file.write_text(content, encoding="utf-8")
    print("Updated index.html nav link")

# 2. Update pages/*.html
for page_file in Path("pages").glob("*.html"):
    content = page_file.read_text(encoding="utf-8")
    # Replace navbar link
    content = re.sub(r'<a href="\.\./index\.html#brands" class="nav-link([^"]*)">Shop</a>', r'<a href="shop.html" class="nav-link\1">Shop</a>', content)
    # Footer link
    content = re.sub(r'<li><a href="\.\./index\.html#brands" class="([^"]*)">Shop</a></li>', r'<li><a href="shop.html" class="\1">Shop</a></li>', content)
    page_file.write_text(content, encoding="utf-8")
    print(f"Updated {page_file}")
