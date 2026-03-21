#!/usr/bin/env python3
"""
Gateway Metal Detectors - RadioWorld Stealth Sync v2.0
Hybrid Solver: Camoufox harvest → curl_cffi replay + JA4 pinning
Preserves ALL original parsing/output logic
"""

import os
import sys
import json
import urllib.parse
import time
import random
import logging
import tempfile
import uuid
import asyncio
import numpy as np
from datetime import datetime, timedelta
from loguru import logger
# import redis
from bs4 import BeautifulSoup
from camoufox import Camoufox as CamouFox  # Keep original name for compatibility in script
from curl_cffi import requests  # pip install curl-cffi
from curl_cffi.requests import Session

# === CONFIG ===
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scraper_v2.log')
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'live_inventory.json')
REDIS_HOST = 'localhost'  # Hostinger Redis addon or local
REDIS_PORT = 6379
REDIS_DB = 0
EXPECTED_THRESHOLD = 50
BRANDS = ['Minelab', 'Garrett', 'Nokta', 'XP Metal Detectors']
IPROYAL_AUTH = "your_iproyal_username:password"  # Residential proxy creds

logger.add(LOG_FILE, level="INFO", rotation="1 week")

# === HYBRID SOLVER CORE (Qwen Parts 1-3) ===
def generate_sticky_proxy():
    """Part 1: IPRoyal sticky session ID"""
    return None

def harvest_token(target_url: str, proxy_str: str) -> dict:
    """Part 1: Camoufox harvest cf_clearance + UA"""
    token_data = {}
    proxy_id = uuid.uuid4().hex[:16]
    redis_key = f"radioworld_token_{proxy_id}"
    
    try:
        with CamouFox(proxy=proxy_str, headless=False, humanize=True, os="windows") as browser:
            browser.get(target_url)
            time.sleep(10)  # Turnstile solve
            
            cookies = browser.get_cookies()
            cf_clearance = next((c['value'] for c in cookies if c['name'] == 'cf_clearance'), None)
            user_agent = browser.user_agent
            
            if cf_clearance and user_agent:
                token_data = {
                    'cf_clearance': cf_clearance,
                    'user_agent': user_agent,
                    'sticky_proxy': proxy_str,
                    'expires_at': (datetime.now() + timedelta(hours=4)).isoformat()
                }
                
                
                # JSON buffer replacement for Redis
                with open('token_buffer.json', 'w') as f:
                    json.dump(token_data, f)
                logger.info(f"Token harvested → JSON Buffer: token_buffer.json")
    except Exception as e:
        logger.error(f"Harvest failed: {e}")
    
    return token_data

def replay_request(redis_key: str, target_url: str) -> str:
    """Part 2: curl_cffi replay w/ JA4 pinning"""
    try:
        with open('token_buffer.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"No token in JSON buffer: {e}")
        return None
    
    cf_clearance = data.get('cf_clearance', '')
    user_agent = data.get('user_agent', '')
    proxy_str = data.get('sticky_proxy', '')
    
    with Session() as session:
        session.cookies.set('cf_clearance', cf_clearance)
        headers = {'User-Agent': user_agent}
        resp = session.get(target_url, headers=headers, impersonate="chrome120", proxy=proxy_str, timeout=45)
        logger.info(f"Replay {target_url} → {resp.status_code}")
        return resp.text

def lognormal_jitter(mean=8.0, variance=1.5):
    """Part 3: Human-like delays (heavy-tailed)"""
    sigma = np.sqrt(np.log(1 + variance))
    mu = np.log(mean) - 0.5 * sigma**2
    delay = np.random.lognormal(mu, sigma)
    return max(1.0, min(90.0, delay))  # Bounds

# === ORIGINAL SCRAPING LOGIC (PRESERVED) ===
def parse_inventory(html_or_json: str, brand: str) -> list:
    """Exact original RadioWorld parsing logic"""
    inventory = []
    
    if html_or_json.startswith('{'):  # API JSON
        data = json.loads(html_or_json)
        items = data.get('items', [])
        
        for prod in items:
            name = prod.get('shortDescription') or prod.get('name', 'Unknown')
            price_data = prod.get('price', {})
            price_amount = price_data.get('listPrice') or price_data.get('amount')
            price_str = f"${price_amount}" if price_amount else "Call for Price"
            
            stock_data = prod.get('stock', {})
            stock_display = stock_data.get('display', {}).get('message', '')
            stock_status = "In Stock" if "In Stock" in stock_display or stock_data.get('available', 0) > 0 else "Out of Stock"
            
            url_slug = prod.get('url', '')
            prod_url = f"https://www.radioworld.ca{url_slug}" if url_slug else ""
            clean_slug = url_slug.split('/')[-1] if url_slug else name.replace(' ', '-').lower()
            
            images = prod.get('images', [])
            image_url = images[0].get('urls', {}).get('large', '') if images else ""
            
            inventory.append({
                "brand": "XP" if "XP " in brand else brand,
                "name": name, "slug": clean_slug, "price": price_str,
                "stock": stock_status, "url": prod_url, "image": image_url
            })
    else:  # HTML fallback (specs)
        soup = BeautifulSoup(html_or_json, 'html.parser')
        # Your original BS4 logic here if needed
        pass
    
    return inventory

def atomic_dump(data, filepath):
    """Original atomic JSON write"""
    temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(filepath), text=True)
    try:
        with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        os.replace(temp_path, filepath)
    finally:
        try: os.remove(temp_path)
        except: pass

# === MAIN LOOP ===
def main():
    logger.info("=== RadioWorld Stealth Sync v2 Starting ===")
    
    # Harvest fresh token
    proxy_str = generate_sticky_proxy()
    harvest_token("https://www.radioworld.ca/metal-detecting/z-md", proxy_str)
    redis_key = "radioworld_token_*"  # Match latest
    
    inventory = []
    for brand in BRANDS:
        brand_encoded = urllib.parse.quote_plus(brand)
        api_url = f"https://www.radioworld.ca/api/search/3/Z-MD?limit=100&termsFilters%5B{brand_encoded}%5D%5Bkey%5D={brand_encoded}&termsFilters%5B{brand_encoded}%5D%5Bname%5D=manufacturer"
        
        html = replay_request(redis_key, api_url)
        time.sleep(lognormal_jitter())  # Human jitter
        
        brand_inventory = parse_inventory(html, brand)
        inventory.extend(brand_inventory)
    
    if len(inventory) < EXPECTED_THRESHOLD:
        logger.error(f"Only {len(inventory)} items - aborting")
        sys.exit(1)
    
    atomic_dump(inventory, OUTPUT_FILE)
    logger.info(f"✅ Synced {len(inventory)} products → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()