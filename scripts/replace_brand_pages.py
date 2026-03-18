import os

pages_dir = r"c:\Projects\Gateway_Final\pages"
targets = {
    "garrett.html": "Garrett",
    "minelab.html": "Minelab",
    "nokta.html": "Nokta Makro",
    "xp.html": "XP Metal Detectors"
}

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0; url=shop.html?brand={brand}">
    <title>Redirecting to Shop - {name}</title>
</head>
<body style="background: black; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; font-family: sans-serif; font-weight: bold; text-transform: uppercase;">
    Redirecting to Unified Shop Interface...
</body>
</html>
"""

for filename, brand_name in targets.items():
    path = os.path.join(pages_dir, filename)
    if os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            # We encode the brand to match the Javascript sidebar query
            url_brand = brand_name
            if brand_name == "Nokta Makro":
                url_brand = "Nokta"
            elif brand_name == "XP Metal Detectors":
                url_brand = "XP"
                
            f.write(html_template.format(brand=url_brand, name=brand_name))
        print(f"Replaced {filename} with redirect to shop.html?brand={url_brand}")
