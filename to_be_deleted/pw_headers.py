from playwright.sync_api import sync_playwright
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    log_file = open("network_headers.log", "w", encoding="utf-8")

    def handle_request(request):
        if request.resource_type in ["xhr", "fetch"]:
            if "api/" in request.url:
                log_file.write(f">>> {request.method} {request.url}\n")
                log_file.write(f"    Headers: {request.headers}\n")

    page.on("request", handle_request)

    url = "https://www.radioworld.ca/metal-detecting/z-md"
    print(f"Navigating to {url}")
    try:
        page.goto(url, wait_until="networkidle", timeout=15000)
    except Exception as e:
        print(f"Timeout or error: {e}")

    page.wait_for_timeout(5000)
    browser.close()
    log_file.close()

with sync_playwright() as playwright:
    run(playwright)
