import cloudscraper

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)

url = "https://www.radioworld.ca/application/modules/core/assets/Angular/Services/HttpService.js?v=200355"
print(f"Fetching {url}")

try:
    response = scraper.get(url, timeout=15)
    print(f"Status Code: {response.status_code}")
    
    with open('http_service.js', 'w', encoding='utf-8') as f:
        f.write(response.text)
        
    print("Saved to http_service.js")
except Exception as e:
    print(f"Error: {e}")
