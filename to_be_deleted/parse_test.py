from bs4 import BeautifulSoup
import re
import json

with open("C:/Projects/Gateway_Final/rw_product.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# look for script tags that contain the dataLayer
scripts = soup.find_all("script")
for s in scripts:
    if s.string and "dataLayer" in s.string and "price" in s.string:
        print("FOUND DATALAYER:")
        print(s.string.strip()[:500])

# look for stock status in the HTML
print("---")
# check if it contains 'in stock' or 'out of stock' text anywhere
body_text = soup.get_text().lower()
if 'in stock' in body_text:
    print("Found 'in stock' text.")
if 'out of stock' in body_text:
    print("Found 'out of stock' text.")

# what about payloads? We saw window.payloads = {};
for s in scripts:
    if s.string and "window.payloads" in s.string:
        print("FOUND PAYLOADS:")
        print(s.string.strip()[:1000])

