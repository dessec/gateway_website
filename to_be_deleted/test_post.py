import cloudscraper
import json

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)

# A sample search URL
url = "https://www.radioworld.ca/metal-detecting/z-md"

try:
    print(f"Testing POST to {url}")
    # The Angular service seems to do a POST to "?" + querystring.
    # We can try just POSTing to the URL
    response = scraper.post(url, headers={'Accept': 'application/json, text/plain, */*'}, timeout=15)
    
    print("Status:", response.status_code)
    print("Headers:", response.headers.get("Content-Type"))
    
    content = response.text
    if len(content) > 500:
        print("Response starts with:", content[:250])
        print("...")
        print("Response ends with:", content[-250:])
    else:
        print("Response:", content)
        
    try:
        data = response.json()
        print("Successfully parsed as JSON!")
        if "results" in data:
            print(f"Found {len(data['results'])} results.")
            if len(data['results']) > 0:
                print("First result title:", data['results'][0].get('title'))
    except Exception as e:
        print("Could not parse as JSON:", type(e).__name__)
        
except Exception as e:
    print(f"Error: {e}")
