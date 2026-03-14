import os
import sys
import json
import time
import random
import logging
import tempfile
import cloudscraper
import urllib.parse

# Configure logging
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scraper.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'live_inventory.json')
EXPECTED_THRESHOLD = 50

# Targets
BRANDS = ['Minelab', 'Garrett', 'Nokta', 'XP Metal Detectors']

def atomic_dump(data, filepath):
    temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(filepath), text=True)
    try:
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, filepath)
    except Exception as e:
        os.remove(temp_path)
        raise e

def scrape_radioworld():
    inventory = []
    
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    headers = {
        'Accept': 'application/json',
        'api-key': 'zs-search',
        'Referer': 'https://www.radioworld.ca/metal-detecting/z-md'
    }
    
    for brand in BRANDS:
        # Build the exact query for each brand exactly as the Next.js/Browser would
        # Limit 100 per manufacturer to ensure we get all products
        brand_encoded = urllib.parse.quote_plus(brand)
        url = f"https://www.radioworld.ca/api/search/3/Z-MD?limit=100&termsFilters%5B{brand_encoded}%5D%5Bkey%5D={brand_encoded}&termsFilters%5B{brand_encoded}%5D%5Bname%5D=manufacturer"
        
        logging.info(f"Targeting {brand} API at {url}")
        
        try:
            resp = scraper.get(url, headers=headers, timeout=30)
            if resp.status_code != 200:
                logging.error(f"API failed for {brand}. Status: {resp.status_code}")
                continue
            
            data = resp.json()
            items = data.get('items', [])
            
            if not items:
                logging.warning(f"No products found for {brand} via API.")
            
            for prod in items:
                name = prod.get('shortDescription', 'Unknown')
                if name == 'Unknown':
                    name = prod.get('name', 'Unknown')
                
                # Format price from amount (e.g. 653.99 -> "$ 653.99")
                price_amount = prod.get('price', {}).get('amount')
                price_str = f"$ {price_amount}" if price_amount is not None else "Call for Price"
                
                # Determine stock status
                stock_data = prod.get('stock', {})
                stock_display = stock_data.get('display', {}).get('message', '')
                
                if "In Stock" in stock_display or stock_data.get('available', 0) > 0:
                    stock_status = "In Stock"
                elif "Out Of Stock" in stock_display or "Sold Out" in stock_display:
                    stock_status = "Out of Stock"
                else:
                    # Default if unknown
                    stock_status = stock_display if stock_display else "Unknown"

                # Link
                url_slug = prod.get('url', '')
                prod_url = url_slug if url_slug.startswith('http') else (f"https://www.radioworld.ca{url_slug}" if url_slug else "https://www.radioworld.ca/manufacturer/")
                
                # Image
                image_url = ""
                images = prod.get('images', [])
                if images and isinstance(images, list) and len(images) > 0:
                    try:
                        image_url = images[0].get('thumbnails', {}).get('small', {}).get('src', '')
                    except:
                        pass
                
                inventory.append({
                    "brand": "XP" if "XP " in brand else brand,
                    "name": name,
                    "price": price_str,
                    "stock": stock_status,
                    "url": prod_url,
                    "image": image_url
                })
                
        except Exception as e:
            logging.error(f"Error processing {brand}: {e}")
            continue

        time.sleep(random.uniform(2, 4))
        
    return inventory

if __name__ == "__main__":
    logging.info("Starting live stock sync...")
    try:
        new_data = scrape_radioworld()
        if len(new_data) < EXPECTED_THRESHOLD:
            logging.warning(f"Sanity check failed: Only {len(new_data)} items parsed. Refusing to overwrite expected {EXPECTED_THRESHOLD}+ items.")
            sys.exit(1)
            
        atomic_dump(new_data, OUTPUT_FILE)
        logging.info(f"Successfully synced {len(new_data)} products to {OUTPUT_FILE}")
        print(f"Success! {len(new_data)} products retrieved.")
    except Exception as e:
        logging.error(f"Fatal script error: {e}")
        sys.exit(1)
