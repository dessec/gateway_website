import re
from pathlib import Path

def fix_links(html):
    html = re.sub(r'<a href="[^"]*?shop\.html"[^>]*>Shop</a>', r'<a href="#brands" class="nav-link">Shop</a>', html)
    html = re.sub(r'<a href="[^"]*?about\.html"[^>]*>About Us</a>', r'<a href="#about" class="nav-link">About Us</a>', html)
    html = re.sub(r'<a href="[^"]*?accessories\.html"[^>]*>Tools</a>', r'<a href="#tools" class="nav-link">Tools</a>', html)
    html = re.sub(r'<a href="[^"]*?cart\.html"[^>]*>Cart</a>', r'<a href="#contact" class="nav-link">Contact</a>', html)
    return html

def fix_links_pages(html):
    html = re.sub(r'<a href="[^"]*?shop\.html"[^>]*>Shop</a>', r'<a href="#inventory-grid" class="nav-link">Shop</a>', html)
    html = re.sub(r'<a href="[^"]*?about\.html"[^>]*>About Us</a>', r'<a href="../index.html#about" class="nav-link">About Us</a>', html)
    html = re.sub(r'<a href="[^"]*?accessories\.html"[^>]*>Tools</a>', r'<a href="../index.html#tools" class="nav-link">Tools</a>', html)
    html = re.sub(r'<a href="[^"]*?cart\.html"[^>]*>Cart</a>', r'<a href="../index.html#contact" class="nav-link">Contact</a>', html)
    html = html.replace("fetch('../live_inventory.json')", "fetch('../scripts/live_inventory.json')")
    return html

f = Path('index.html')
if f.exists():
    f.write_text(fix_links(f.read_text('utf-8')), 'utf-8')

for p in Path('pages').glob('*.html'):
    p.write_text(fix_links_pages(p.read_text('utf-8')), 'utf-8')
