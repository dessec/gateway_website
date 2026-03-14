import cloudscraper
import json

scraper = cloudscraper.create_scraper()

brand = "Nokta"
url = f"https://www.radioworld.ca/api/search/3/Z-MD?limit=100&termsFilters%5B{brand}%5D%5Bkey%5D={brand}&termsFilters%5B{brand}%5D%5Bname%5D=manufacturer"

headers = {
    'Accept': 'application/json',
    'api-key': 'zs-search',
    'Referer': 'https://www.radioworld.ca/metal-detecting/z-md'
}

try:
    print(f"Testing GET to {url}")
    response = scraper.get(url, headers=headers, timeout=30)
    
    print("Status:", response.status_code)
    
    try:
        data = response.json()
        print("Successfully parsed as JSON!")
        
        if 'search' in data:
            results = data['search'].get('results', [])
            print(f"Found {len(results)} results.")
            if len(results) > 0:
                for i in range(min(5, len(results))):
                    print(f"Result {i+1}: {results[i].get('partNumber')} - {results[i].get('title')}")
                    print(f"  Price: {results[i].get('price', {}).get('amount')}")
                    print(f"  Stock: {results[i].get('stock', {}).get('display', {}).get('message')}")
        else:
            print("Keys in JSON:", list(data.keys()))
            
    except Exception as e:
        print("Could not parse as JSON:", type(e).__name__)
        
except Exception as e:
    print(f"Error: {e}")
