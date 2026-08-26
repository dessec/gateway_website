import os
import re
import glob

# The replacement script
purechat_script = """<script type='text/javascript' data-cfasync='false'>window.purechatApi = { l: [], t: [], on: function () { this.l.push(arguments); } }; (function () { var done = false; var script = document.createElement('script'); script.async = true; script.type = 'text/javascript'; script.src = 'https://app.purechat.com/VisitorWidget/WidgetScript'; document.getElementsByTagName('HEAD').item(0).appendChild(script); script.onreadystatechange = script.onload = function (e) { if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete')) { var w = new PCWidget({c: '76adb4c9-78ac-4ea9-b7b3-36e4412eca7d', f: true }); done = true; } }; })();</script>"""

html_files = []
# Find all HTML files in current directory and pages/ directory
html_files.extend(glob.glob('*.html'))
html_files.extend(glob.glob('pages/*.html'))

for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regular expression to match Tawk.to script block
        # Using DOTALL so that .* matches newlines
        pattern = re.compile(r'<!--Start of Tawk\.to Script-->.*?<!--End of Tawk\.to Script-->', re.DOTALL)
        
        if pattern.search(content):
            new_content = pattern.sub(purechat_script, content)
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print(f"Replaced string in {html_file}")
        else:
            print(f"No match found in {html_file}")
            
    except Exception as e:
        print(f"Error processing {html_file}: {e}")
