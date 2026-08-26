import os
import glob

old_script = """<script type='text/javascript' data-cfasync='false'>window.purechatApi = { l: [], t: [], on: function () { this.l.push(arguments); } }; (function () { var done = false; var script = document.createElement('script'); script.async = true; script.type = 'text/javascript'; script.src = 'https://app.purechat.com/VisitorWidget/WidgetScript'; document.getElementsByTagName('HEAD').item(0).appendChild(script); script.onreadystatechange = script.onload = function (e) { if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete')) { var w = new PCWidget({c: '76adb4c9-78ac-4ea9-b7b3-36e4412eca7d', f: true }); done = true; } }; })();</script>"""

new_script = """<script>
window.replainSettings = { id: '49635770-b7b9-49c1-bb08-348efe34892c' };
(function(u){var s=document.createElement('script');s.async=true;s.src=u;
var x=document.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);
})('https://widget.replain.cc/dist/client.js');
</script>"""

html_files = glob.glob('*.html') + glob.glob('pages/*.html')

replaced_count = 0

for filepath in html_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_script in content:
            new_content = content.replace(old_script, new_script)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Replaced Purechat with Re:plain in {filepath}")
            replaced_count += 1
        else:
            print(f"Purechat script not found in {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print(f"\nTotal files updated: {replaced_count}")
