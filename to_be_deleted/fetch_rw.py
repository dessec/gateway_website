import cloudscraper

url = "https://www.radioworld.ca/product/nokta-11000705/simplex-lite-with-sx28-coil"
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

try:
    resp = scraper.get(url, timeout=15)
    resp.raise_for_status()
    with open("C:/Projects/Gateway_Final/rw_product.html", "w", encoding="utf-8") as f:
        f.write(resp.text)
    print("Downloaded snippet.")
except Exception as e:
    print(f"Failed: {e}")
