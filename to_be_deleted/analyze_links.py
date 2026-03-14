import os
import re
from pathlib import Path

def find_asset_references():
    html_files = list(Path('.').glob('*.html'))
    css_files = list(Path('.').glob('*.css'))
    
    referenced = set()
    
    # Regex to catch src="..." and href="..."
    patterns = [
        re.compile(r'src=["\']([^"\']+)["\']', re.IGNORECASE),
        re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE),
        re.compile(r'url\(["\']?([^"\')]+)["\']?\)', re.IGNORECASE)
    ]
    
    for f in html_files + css_files:
        content = f.read_text(encoding='utf-8')
        for p in patterns:
            matches = p.findall(content)
            for m in matches:
                # ignore external urls, data URIs, anchor links
                if m.startswith('http') or m.startswith('data:') or m.startswith('#') or m == '/':
                    continue
                referenced.add(m)
                
    print("Referenced local files:")
    for r in sorted(referenced):
        print(f" - {r}")

if __name__ == '__main__':
    find_asset_references()
