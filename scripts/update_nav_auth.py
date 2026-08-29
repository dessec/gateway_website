"""
Batch-update all Gateway HTML files:
1. Inject Supabase CDN + gateway-auth.js + auth-modal.js into <head>
2. Remodel <nav> to three-column layout with auth-cart-container
"""
import re, os, glob

ROOT = r'c:\Projects\Gateway_Final'

# Files to process
files = [os.path.join(ROOT, 'index.html')]
pages_dir = os.path.join(ROOT, 'pages')
for f in glob.glob(os.path.join(pages_dir, '*.html')):
    basename = os.path.basename(f)
    # Skip new files we just created (they already have the new structure)
    if basename in ('checkout.html', 'profile.html'):
        continue
    files.append(f)

def get_script_prefix(filepath):
    """Return the relative path prefix for scripts/ and assets/ based on file location."""
    if 'pages' in filepath.replace('\\', '/'):
        return '../'
    return ''

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    prefix = get_script_prefix(filepath)
    basename = os.path.basename(filepath)
    
    # ─── 1. Inject Supabase CDN into <head> (after tailwindcss script) ───
    supabase_cdn = '<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>'
    if 'supabase-js@2' not in content:
        # Insert after the tailwindcss CDN line
        content = content.replace(
            '<script src="https://cdn.tailwindcss.com"></script>',
            '<script src="https://cdn.tailwindcss.com"></script>\n    ' + supabase_cdn,
            1
        )
    
    # ─── 2. Inject gateway-auth.js and auth-modal.js before </body> ───
    auth_scripts = f'<script src="{prefix}scripts/gateway-auth.js"></script>\n<script src="{prefix}scripts/auth-modal.js"></script>'
    if 'gateway-auth.js' not in content:
        # Insert before the purechat script or before </body>
        if "purechatApi" in content:
            content = content.replace(
                "<script type='text/javascript' data-cfasync='false'>window.purechatApi",
                auth_scripts + "\n<script type='text/javascript' data-cfasync='false'>window.purechatApi",
                1
            )
        else:
            content = content.replace('</body>', auth_scripts + '\n</body>', 1)
    
    # ─── 3. Remodel the <nav> to three-column layout ───
    # We need to:
    # a) Add auth-cart-container div after the nav links div
    # b) Make nav links truly centered with absolute positioning
    
    # Add auth-cart-container if not present
    if 'auth-cart-container' not in content:
        # Find the closing </div> of the nav links and the </nav> tag
        # The pattern is: </div>\n    </nav>
        # We insert our auth container between them
        
        # For nav links div, we look for the pattern ending the Center Nav Links div
        # and insert our auth container after it
        nav_end_pattern = re.compile(
            r'(<!--\s*Center Nav Links\s*-->.*?</div>)\s*\n(\s*</nav>)',
            re.DOTALL
        )
        match = nav_end_pattern.search(content)
        if match:
            replacement = match.group(1) + '\n        <div id="auth-cart-container" class="hidden lg:flex items-center"></div>\n' + match.group(2)
            content = content[:match.start()] + replacement + content[match.end():]
    
    # ─── 4. Center nav links with absolute positioning ───
    # Change the nav links div to use absolute centering
    # Current: class="hidden lg:flex items-center space-x-6"
    # New: class="hidden lg:flex items-center space-x-6 absolute left-1/2 -translate-x-1/2"
    
    if 'absolute left-1/2 -translate-x-1/2' not in content:
        # Only modify the nav links div, not other divs
        # Look for the specific pattern after <!-- Center Nav Links -->
        content = re.sub(
            r'(<!--\s*Center Nav Links\s*-->\s*\n\s*<div class="hidden lg:flex items-center space-x-6)"',
            r'\1 absolute left-1/2 -translate-x-1/2"',
            content,
            count=1
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  [OK] {basename}')

print('Updating Gateway HTML files...\n')
for filepath in files:
    try:
        process_file(filepath)
    except Exception as e:
        print(f'  [ERR] {os.path.basename(filepath)}: {e}')

print(f'\nDone! Updated {len(files)} files.')
