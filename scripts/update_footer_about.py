import re
from pathlib import Path

new_about_text = """<p class="text-xs text-gray-600 font-semibold leading-relaxed mb-8">
                    <span class="text-gray-900 font-bold">ABOUT US:</span> Gateway Metal Detectors is Hamilton's dedicated treasure hunting hub, founded on a lifelong passion for discovery. We carry professional-grade equipment from the world's leading brands — Nokta, Minelab, XP, and Garrett. Whether you're a first-time hobbyist or a seasoned detectorist, we have the gear and the knowledge to back it up. Serving Southern Ontario and shipping across Canada and worldwide.
                </p>"""

pattern = re.compile(r'<p class="text-xs text-gray-\d+ font-semibold leading-relaxed mb-8">\s*<span class="text-(?:gray-900|white) font-bold">ABOUT US:</span>.*?</p>', re.DOTALL)

files_to_update = [Path("index.html")] + list(Path("pages").glob("*.html"))

for file_path in files_to_update:
    content = file_path.read_text(encoding="utf-8")
    if pattern.search(content):
        updated = pattern.sub(new_about_text, content)
        file_path.write_text(updated, encoding="utf-8")
        print(f"Updated {file_path}")
    else:
        print(f"Pattern NOT found in {file_path}")
