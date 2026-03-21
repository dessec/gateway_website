#!/usr/bin/env python3
"""
Builds product_data.json from the local 'Product Data' folder.
Maps product slugs to local images, descriptions, and specs.
Run this locally whenever new product data is added.
"""

import os
import json
import glob
import re

PRODUCT_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'Product Data')
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'product_data.json')
ASSETS_BASE = '../assets/Product Data'  # Path relative to pages/ for the browser

def folder_to_slug(folder_name: str) -> list[str]:
    """Generate multiple possible slug variants from a folder name."""
    # e.g. "Garrett_Vortex_VX5" -> "vortex-vx-5-metal-detector", "vortex-vx5", etc.
    # Strip brand prefix
    name = re.sub(r'^(Garrett|Nokta|Minelab|XP)[_ ]', '', folder_name, flags=re.IGNORECASE)
    # Convert underscores/spaces to hyphens, lowercase
    slug = name.replace('_', '-').replace(' ', '-').lower()
    # Also make a version without hyphens between letters and numbers
    variants = [slug]
    # vortex-vx5 → vortex-vx-5  and vice versa
    alt = re.sub(r'([a-z])(\d)', r'\1-\2', slug)
    if alt != slug:
        variants.append(alt)
    alt2 = re.sub(r'-(\d)', r'\1', slug)
    if alt2 != slug:
        variants.append(alt2)
    return variants

def build_index():
    index = {}
    product_dirs = [d for d in os.listdir(PRODUCT_DATA_DIR) 
                    if os.path.isdir(os.path.join(PRODUCT_DATA_DIR, d))]

    for folder in product_dirs:
        folder_path = os.path.join(PRODUCT_DATA_DIR, folder)
        json_path = os.path.join(folder_path, 'FULL_specs_description.json')

        if not os.path.exists(json_path):
            continue

        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)

        # Collect all image files in this folder, sorted
        image_files = sorted(glob.glob(os.path.join(folder_path, 'pro_image_*.jpg')))
        image_paths = [f'{ASSETS_BASE}/{folder}/{os.path.basename(img)}' for img in image_files]

        entry = {
            'model': folder,
            'brand': data.get('brand', ''),
            'description': data.get('description', ''),
            'detailed_specs': data.get('detailed_specs', {}),
            'images': image_paths,
        }

        # Register under all slug variants
        for slug in folder_to_slug(folder):
            if slug not in index:
                index[slug] = entry
        
        # Also register under a slug derived from the model title if available
        title = data.get('title', '')
        if title:
            title_slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            # Take just the first 50 chars to keep it reasonable
            if title_slug and title_slug not in index:
                index[title_slug] = entry

        print(f"  ✔ {folder} → {folder_to_slug(folder)}")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Built product_data.json with {len(index)} slug entries from {len(product_dirs)} product folders.")

if __name__ == '__main__':
    build_index()
