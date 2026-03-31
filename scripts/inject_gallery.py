import os
import glob
import re

files = glob.glob('**/*.html', recursive=True)

for f in files:    
    if 'gallery.html' in f: continue

    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
        
    content = content.replace('\r\n', '\n')
    
    # 1. Fix global broken anchor links first!
    content = content.replace('href="../index.html#about"', 'href="about.html"')
    content = content.replace('href="index.html#about"', 'href="pages/about.html"')
    content = content.replace('href="../index.html#contact"', 'href="contact.html"')
    content = content.replace('href="index.html#contact"', 'href="pages/contact.html"')
    
    # 2. Fix inner footer anchor link shortcuts
    content = content.replace('href="#about"', 'href="pages/about.html"')
    content = content.replace('href="#contact"', 'href="pages/contact.html"')

    # 3. Inject Gallery
    if 'index.html' in f:
        nav_find = r'(<a href="pages/contact\.html" class="nav-link(?: active)?">Contact</a>)'
        nav_repl = r'<a href="pages/gallery.html" class="nav-link">Gallery</a>\n            <span class="text-gray-300">-</span>\n            \1'
        content = re.sub(nav_find, nav_repl, content)
        
        foot_find = r'(<li><a href="pages/community-map\.html"\s*class="hover:text-white transition cursor-pointer inline-block">Maps</a></li>)'
        foot_repl = r'\1\n                    <li><a href="pages/gallery.html" class="hover:text-white transition cursor-pointer inline-block">Gallery</a></li>'
        content = re.sub(foot_find, foot_repl, content)
        
    else:
        nav_find = r'(<a href="contact\.html" class="nav-link(?: active)?">Contact</a>)'
        nav_repl = r'<a href="gallery.html" class="nav-link">Gallery</a>\n            <span class="text-gray-300">-</span>\n            \1'
        content = re.sub(nav_find, nav_repl, content)
        
        foot_find = r'(<li><a href="community-map\.html"\s*class="hover:text-white transition cursor-pointer inline-block">Maps</a></li>)'
        foot_repl = r'\1\n                    <li><a href="gallery.html" class="hover:text-white transition cursor-pointer inline-block">Gallery</a></li>'
        content = re.sub(foot_find, foot_repl, content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Absolute Fix Complete.")
