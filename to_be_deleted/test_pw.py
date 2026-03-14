from playwright.sync_api import sync_playwright
import time

def test_scrape():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        # Use a user agent to look like a real browser
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
        page = context.new_page()
        
        print("Navigating...")
        page.goto('https://www.radioworld.ca/manufacturer/97/Minelab', wait_until='networkidle')
        
        # Wait for the product cards to be populated by JS
        print("Waiting for products...")
        try:
            # Look for typical product card elements
            page.wait_for_selector('.product-card, .card, .product-layout, .partnum-title', timeout=15000)
            time.sleep(2) # Give it an extra second after selector appears
        except Exception as e:
            print("Timeout waiting for products or they don't exist.")
        
        print("Extracting...")
        # Print a sample of the page content
        content = page.content()
        if 'EQUINOX 700' in content or 'EQUINOX 900' in content:
            print("SUCCESS: Found Equinox in page content!")
        else:
            print("FAILED: Could not find Equinox. Maybe Cloudflare blocked?")
            
        print("Number of .card elements:")
        cards = page.query_selector_all('.card')
        print(len(cards))
        
        browser.close()

if __name__ == "__main__":
    test_scrape()
