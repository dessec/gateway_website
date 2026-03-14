import os
import re
import shutil
from pathlib import Path

def setup_directories():
    base = Path('C:/Projects/Gateway_Final')
    dirs = ['assets/images', 'scripts', 'styles', 'future_assets', 'to_be_deleted', 'pages']
    for d in dirs:
        (base / d).mkdir(parents=True, exist_ok=True)
    return base

def move_file(src, dest):
    if src.exists():
        if dest.exists() and src.samefile(dest):
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        print(f"Moved: {src.name} -> {dest.relative_to(Path('C:/Projects/Gateway_Final'))}")

def restructure():
    base = setup_directories()
    
    # 1. Styles
    move_file(base / 'style.css', base / 'styles' / 'style.css')
    
    # 2. Scripts
    move_file(base / 'radioworld_sync.py', base / 'scripts' / 'radioworld_sync.py')
    
    # 3. Active Images -> assets/images
    active_images = [
        'assets/Hero_River_2.jpg',
        'assets/Map_Pin.png',
        'assets/identifier_tool_cinematic.png',
        'assets/Brand Cards/Rough Copy/Garret.png',
        'assets/Brand Cards/Rough Copy/Nokta.png',
        'assets/Brand Cards/Rough Copy/XP.png',
        'assets/1-9 Structure/2nd.png',
        'assets/1-9 Structure/4th.png'
    ]
    for img in active_images:
        src = base / img
        if src.exists():
            move_file(src, base / 'assets/images' / src.name)
            
    # Move remaining assets to future_assets
    # We only move the contents of the assets folder that aren't the new 'images' folder
    assets_dir = base / 'assets'
    for item in assets_dir.iterdir():
        if item.name == 'images':
            continue
        move_file(item, base / 'future_assets' / item.name)

    # 4. HTML Pages
    pages = ['garrett.html', 'nokta.html', 'xp.html', 'community-clubs.html', 'community-map.html']
    for p in pages:
        move_file(base / p, base / 'pages' / p)
        
    # 5. Logs to to_be_deleted
    logs = ['scraper.log', 'analyze_links.py']
    for l in logs:
        move_file(base / l, base / 'to_be_deleted' / l)

def update_references():
    base = Path('C:/Projects/Gateway_Final')
    
    # Map old paths to new paths (relative to root)
    path_map = {
        'style.css': 'styles/style.css',
        'assets/Hero_River_2.jpg': 'assets/images/Hero_River_2.jpg',
        'assets/Map_Pin.png': 'assets/images/Map_Pin.png',
        'assets/identifier_tool_cinematic.png': 'assets/images/identifier_tool_cinematic.png',
        'assets/Brand Cards/Rough Copy/Garret.png': 'assets/images/Garret.png',
        'assets/Brand Cards/Rough Copy/Nokta.png': 'assets/images/Nokta.png',
        'assets/Brand Cards/Rough Copy/XP.png': 'assets/images/XP.png',
        'assets/1-9 Structure/2nd.png': 'assets/images/2nd.png',
        'assets/1-9 Structure/4th.png': 'assets/images/4th.png',
        'garrett.html': 'pages/garrett.html',
        'nokta.html': 'pages/nokta.html',
        'xp.html': 'pages/xp.html',
        'community-clubs.html': 'pages/community-clubs.html',
        'community-map.html': 'pages/community-map.html'
    }

    # Encode URLs for reliable replacement
    def normalize_link(link):
        return link.replace('%20', ' ')

    # Update files in root (index.html, etc)
    for root_file in base.glob('*.html'):
        content = root_file.read_text(encoding='utf-8')
        new_content = content
        for old, new in path_map.items():
            # Replace exact matches.
            # Handle cases where old path might have URL encoding
            old_encoded = old.replace(' ', '%20')
            new_encoded = new.replace(' ', '%20')
            
            new_content = new_content.replace(f'"{old}"', f'"{new}"')
            new_content = new_content.replace(f"'{old}'", f"'{new}'")
            new_content = new_content.replace(f'"{old_encoded}"', f'"{new_encoded}"')
            new_content = new_content.replace(f"'{old_encoded}'", f"'{new_encoded}'")
            new_content = new_content.replace(f'url("{old}")', f'url("{new}")')
            new_content = new_content.replace(f"url('{old}')", f"url('{new}')")
            new_content = new_content.replace(f'url("{old_encoded}")', f'url("{new_encoded}")')
            new_content = new_content.replace(f"url('{old_encoded}')", f"url('{new_encoded}')")

        root_file.write_text(new_content, encoding='utf-8')
        print(f"Updated references in {root_file.name}")

    # Update files in pages/
    for page_file in (base / 'pages').glob('*.html'):
        content = page_file.read_text(encoding='utf-8')
        new_content = content
        
        # In pages, links to root need ../
        # index.html -> ../index.html
        new_content = re.sub(r'(href|src)=["\']index\.html["\']', r'\1="../index.html"', new_content)
        
        # community-map.html fetches save-pin.php
        new_content = new_content.replace("'save-pin.php'", "'../save-pin.php'")
        new_content = new_content.replace('"save-pin.php"', '"../save-pin.php"')
        
        # update paths using the map, adding ../ prefix since these are now in pages/
        for old, new in path_map.items():
            new_rel = f"../{new}"
            old_encoded = old.replace(' ', '%20')
            new_rel_encoded = new_rel.replace(' ', '%20')
            
            new_content = new_content.replace(f'"{old}"', f'"{new_rel}"')
            new_content = new_content.replace(f"'{old}'", f"'{new_rel}'")
            new_content = new_content.replace(f'"{old_encoded}"', f'"{new_rel_encoded}"')
            new_content = new_content.replace(f"'{old_encoded}'", f"'{new_rel_encoded}'")
            new_content = new_content.replace(f'url("{old}")', f'url("{new_rel}")')
            new_content = new_content.replace(f"url('{old}')", f"url('{new_rel}')")
            new_content = new_content.replace(f'url("{old_encoded}")', f'url("{new_rel_encoded}")')
            new_content = new_content.replace(f"url('{old_encoded}')", f"url('{new_rel_encoded}')")

            # Also handle if the page linked to another page directly (e.g. garrett.html instead of pages/garrett.html)
            # Since they are both in the pages folder now, just the filename is enough
            new_content = new_content.replace(f'"../pages/{Path(old).name}"', f'"{Path(old).name}"')
            new_content = new_content.replace(f"'../pages/{Path(old).name}'", f"'{Path(old).name}'")

        page_file.write_text(new_content, encoding='utf-8')
        print(f"Updated references in pages/{page_file.name}")
        
    # Update style.css (now in styles/ relative to images in assets/images/)
    css_file = base / 'styles' / 'style.css'
    if css_file.exists():
        content = css_file.read_text(encoding='utf-8')
        new_content = content
        # CSS is in styles/, images in assets/images/. 
        # Example: url("assets/Hero_River_2.jpg") -> url("../assets/images/Hero_River_2.jpg")
        for old, new in path_map.items():
            if new.startswith('assets/images/'):
                new_rel = f"../{new}"
                old_encoded = old.replace(' ', '%20')
                new_rel_encoded = new_rel.replace(' ', '%20')
                
                new_content = new_content.replace(f'url("{old}")', f'url("{new_rel}")')
                new_content = new_content.replace(f"url('{old}')", f"url('{new_rel}')")
                new_content = new_content.replace(f'url("{old_encoded}")', f'url("{new_rel_encoded}")')
                new_content = new_content.replace(f"url('{old_encoded}')", f"url('{new_rel_encoded}')")
                new_content = new_content.replace(f'url({old})', f'url({new_rel})')
                new_content = new_content.replace(f'url({old_encoded})', f'url({new_rel_encoded})')
        css_file.write_text(new_content, encoding='utf-8')
        print("Updated references in styles/style.css")

if __name__ == "__main__":
    print("Starting restructuring...")
    restructure()
    print("Updating references...")
    update_references()
    print("Execution complete.")
