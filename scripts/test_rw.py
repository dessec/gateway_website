import cloudscraper
import json

scraper = cloudscraper.create_scraper()

url = "https://www.radioworld.ca/product/grt-1142860/vortex-vx-5-metal-detector"
headers = {'User-Agent': 'Mozilla/5.0'}

resp = scraper.get(url, headers=headers)
html = resp.text

# Let's search for "window.BCData" or JSON-LD
if 'application/ld+json' in html:
    print("Found JSON LD!")
    
# Let's search for some generic spec keywords
if 'Specifications' in html:
    print("HTML contains 'Specifications'")
    
# Let's just dump a chunk of text around the description
idx = html.find('tab-description')
if idx != -1:
    print(html[idx:idx+1000])
else:
    # Try finding typical BigCommerce or Lightspeed description class
    idx2 = html.find('productView-description')
    if idx2 != -1:
        print(html[idx2:idx2+1000])
    
