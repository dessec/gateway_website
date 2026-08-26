import re
from pathlib import Path

def fix_shop_link_root(html):
    return re.sub(r'<a href="[^"]*?" class="nav-link(.*?)>Shop</a>', r'<a href="#brands" class="nav-link\1>Shop</a>', html)

def fix_shop_link_pages(html):
    return re.sub(r'<a href="[^"]*?" class="nav-link(.*?)>Shop</a>', r'<a href="../index.html#brands" class="nav-link\1>Shop</a>', html)

f = Path('index.html')
if f.exists():
    f.write_text(fix_shop_link_root(f.read_text('utf-8')), 'utf-8')

for p in Path('pages').glob('*.html'):
    p.write_text(fix_shop_link_pages(p.read_text('utf-8')), 'utf-8')
