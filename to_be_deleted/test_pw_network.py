from playwright.sync_api import sync_playwright
import time
import json

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    log_file = open("network.log", "w", encoding="utf-8")

    def handle_request(request):
        if request.resource_type in ["xhr", "fetch"]:
            log_file.write(f">>> {request.method} {request.url}\n")
            if request.post_data:
                log_file.write(f"    Body: {request.post_data}\n")

    def handle_response(response):
        if response.request.resource_type in ["xhr", "fetch"]:
            log_file.write(f"<<< {response.status} {response.url}\n")
            if "application/json" in response.headers.get("content-type", ""):
                try:
                    data = response.json()
                    log_file.write(f"    JSON keys: {list(data.keys())}\n")
                    if "results" in data:
                        log_file.write(f"    Found {len(data['results'])} results!\n")
                        if len(data['results']) > 0:
                            log_file.write(f"    First result: {data['results'][0].get('title')}\n")
                except Exception as e:
                    pass
            log_file.flush()

    page.on("request", handle_request)
    page.on("response", handle_response)

    url = "https://www.radioworld.ca/metal-detecting/z-md"
    log_file.write(f"Navigating to {url}\n")
    try:
        page.goto(url, wait_until="networkidle", timeout=15000)
    except Exception as e:
        log_file.write(f"Timeout or error: {e}\n")

    page.wait_for_timeout(5000)

    browser.close()
    log_file.close()

with sync_playwright() as playwright:
    run(playwright)
