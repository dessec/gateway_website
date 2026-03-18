import os
import re

pages_dir = r"c:\Projects\Gateway_Final\pages"
targets = {
    "garrett.html": "Garrett",
    "minelab.html": "Minelab",
    "nokta.html": "Nokta Makro",
    "xp.html": "XP Metal Detectors"
}

SIDEBAR_HTML = """    <!-- Shop Layout with Sidebar & Dense Grid -->
    <div class="w-full flex-grow flex flex-col md:flex-row max-w-[1700px] mx-auto pt-6 px-4 md:px-8 bg-[#fcfcfc]">
        
        <!-- Left Sidebar (Filters) -->
        <aside class="w-full md:w-64 lg:w-72 shrink-0 pr-0 md:pr-8 mb-8 md:mb-0">
            <div class="sticky top-28 max-h-[calc(100vh-120px)] overflow-y-auto custom-scrollbar pr-2 pb-10">
                <h2 class="text-lg font-black uppercase tracking-widest text-black mb-8 border-b border-gray-200 pb-4">Filters</h2>
                
                <!-- Category Filter -->
                <div class="mb-8">
                    <h3 class="text-[11px] font-bold uppercase tracking-widest text-gray-400 mb-4">Category</h3>
                    <div class="space-y-3">
                        <label class="flex items-center gap-3 cursor-pointer group">
                            <input type="checkbox" class="filter-checkbox filter-category" value="detectors">
                            <span class="text-sm font-semibold text-gray-700 group-hover:text-black transition-colors">Detectors</span>
                        </label>
                        <label class="flex items-center gap-3 cursor-pointer group">
                            <input type="checkbox" class="filter-checkbox filter-category" value="coils">
                            <span class="text-sm font-semibold text-gray-700 group-hover:text-black transition-colors">Coils</span>
                        </label>
                        <label class="flex items-center gap-3 cursor-pointer group">
                            <input type="checkbox" class="filter-checkbox filter-category" value="accessories">
                            <span class="text-sm font-semibold text-gray-700 group-hover:text-black transition-colors">Accessories</span>
                        </label>
                        <label class="flex items-center gap-3 cursor-pointer group">
                            <input type="checkbox" class="filter-checkbox filter-category" value="parts">
                            <span class="text-sm font-semibold text-gray-700 group-hover:text-black transition-colors">Cables & Parts</span>
                        </label>
                    </div>
                </div>

                <!-- Price Filter -->
                <div class="mb-8">
                    <h3 class="text-[11px] font-bold uppercase tracking-widest text-gray-400 mb-4">Price Range</h3>
                    <div class="space-y-3">
                        <label class="flex items-center gap-3 cursor-pointer group">
                            <input type="checkbox" class="filter-checkbox filter-price" value="under-500">
                            <span class="text-sm font-semibold text-gray-700 group-hover:text-black transition-colors">Under $500</span>
                        </label>
                        <label class="flex items-center gap-3 cursor-pointer group">
                            <input type="checkbox" class="filter-checkbox filter-price" value="500-1000">
                            <span class="text-sm font-semibold text-gray-700 group-hover:text-black transition-colors">$500 - $1,000</span>
                        </label>
                        <label class="flex items-center gap-3 cursor-pointer group">
                            <input type="checkbox" class="filter-checkbox filter-price" value="over-1000">
                            <span class="text-sm font-semibold text-gray-700 group-hover:text-black transition-colors">Over $1,000</span>
                        </label>
                    </div>
                </div>

                <!-- Stock Filter -->
                <div class="mb-8">
                    <h3 class="text-[11px] font-bold uppercase tracking-widest text-gray-400 mb-4">Availability</h3>
                    <div class="space-y-3">
                        <label class="flex items-center gap-3 cursor-pointer group">
                            <input type="checkbox" class="filter-checkbox filter-stock" value="in-stock">
                            <span class="text-sm font-semibold text-gray-700 group-hover:text-black transition-colors">In Stock Only</span>
                        </label>
                    </div>
                </div>

                <!-- Clear Filters -->
                <button id="clear-filters" class="w-full py-3 bg-gray-100 text-gray-600 font-bold uppercase tracking-widest text-[10px] hover:bg-gray-200 transition-colors">
                    Clear All Filters
                </button>
            </div>
        </aside>

        <!-- Right Content & Dense Grid -->
        <main class="w-full flex-grow pb-32">
            
            <div class="flex items-center justify-between mb-6 pb-4 border-b border-gray-200">
                <h1 class="text-3xl font-bold font-serif text-black tracking-tight" style="font-family: Georgia, serif;">{brand} Inventory</h1>
                <p id="product-count" class="text-sm font-bold text-gray-400 tracking-widest uppercase">Loading...</p>
            </div>

            <!-- Loading State -->
            <div id="loading" class="w-full py-32 flex flex-col justify-center items-center">
                <div class="w-8 h-8 rounded-full border-2 border-dashed border-gray-400 animate-spin mb-4"></div>
                <p class="text-xs font-bold uppercase tracking-widest text-gray-500">Syncing Inventory...</p>
            </div>

            <!-- 5-Column Grid -->
            <div id="inventory-grid" class="hidden grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
                <!-- Javascript will inject sharp product cards here -->
            </div>

            <div id="no-results" class="hidden w-full py-32 flex flex-col items-center justify-center border border-dashed border-gray-300">
                <p class="text-lg font-bold text-gray-400 tracking-tight mb-2">No products match your filters.</p>
                <button onclick="document.getElementById('clear-filters').click()" class="text-sm text-black underline font-semibold">Clear Filters</button>
            </div>

        </main>
    </div>
"""

NEW_SCRIPT = """    <script>
        // Data globals
        let allProducts = [];

        // Helper: Is Bundle?
        function isBundleItem(item) {
            const name = (item.name || '').toLowerCase();
            const url  = (item.url  || '').toLowerCase();
            const bundleKeywords = [
                'bundle', 'pro-pack', 'propack', 'pro pack',
                'expedition pack', 'beginner pack', 'package',
                ' kit', '-kit', ' pack', '-pack', 'combo', 'deal',
                'accessory package', 'starter accessory', 'advantage accessory',
                'adventure accessory'
            ];
            return bundleKeywords.some(kw => name.includes(kw) || url.includes(kw));
        }

        // Helper: Classifier
        function getCategory(item) {
            const name = (item.name || '').toLowerCase();
            const url  = (item.url  || '').toLowerCase();
            const text = name + ' ' + url;

            if (text.includes('coil') || text.includes('searchcoil')) return 'coils';
            if (text.includes('metal detector') || text.includes('treasure detector') ||
                text.includes('gold detector') || /\b(simplex|legend|score|findx|hoard|vortex|axiom|ace |ace-|apex|atpro|atmax|at pro|at max|at gold|goldmaster|equinox|manticore|vanquish|ctx|gpx|gpz|sdc|gold monster|x-terra|deus)\b/i.test(name))
                return 'detectors';

            if (text.includes('cable') || text.includes('shaft') || text.includes('charger') ||
                text.includes('replacement') || text.includes('mounting') || text.includes('battery') ||
                text.includes('cover') || text.includes('upgrade code') || text.includes('cuff') ||
                text.includes('armrest') || text.includes('bolt') || text.includes('hardware'))
                return 'parts';

            return 'accessories';
        }

        // Helper: Convert Price String to Number
        function extractPrice(priceStr) {
            if (!priceStr || priceStr.toLowerCase().includes('call')) return null;
            const numeric = parseFloat(priceStr.replace(/[^0-9.]/g, ''));
            return isNaN(numeric) ? null : numeric;
        }

        // DOM Elements
        const grid = document.getElementById('inventory-grid');
        const loading = document.getElementById('loading');
        const countDisplay = document.getElementById('product-count');
        const noResults = document.getElementById('no-results');

        // Render Function
        function renderGrid(productsToRender) {
            countDisplay.innerText = `${productsToRender.length} Products`;
            
            if (productsToRender.length === 0) {
                grid.classList.add('hidden');
                noResults.classList.remove('hidden');
                grid.innerHTML = '';
                return;
            }

            noResults.classList.add('hidden');
            grid.classList.remove('hidden');

            grid.innerHTML = productsToRender.map(item => {
                const isOutOfStock = item.stock.toLowerCase().includes('out') || item.stock.toLowerCase().includes('sold');
                const stockDot = isOutOfStock ? 'bg-red-500' : 'bg-green-500';
                const stockText = isOutOfStock ? 'text-red-500' : 'text-green-600';
                
                // Keep UI dense: Image container, short details below. Minimal padding. No rounded corners. No buttons.
                return `
                <a href="product.html?id=${item.slug}" class="product-card">
                    <div class="img-container border-b border-gray-100">
                        ${item.image ? `<img src="${item.image}" alt="${item.name}" loading="lazy">` : `<div class="text-gray-300 font-bold uppercase tracking-widest text-[10px] w-full h-full flex items-center justify-center bg-gray-50">No Image</div>`}
                    </div>
                    <div class="textContainer gap-1">
                        <p class="text-[9px] font-black uppercase tracking-widest text-gray-400 mb-0.5">${item.brand}</p>
                        <h3 class="text-sm font-bold text-black leading-snug mb-2 flex-grow">${item.name}</h3>
                        
                        <div class="flex items-center justify-between mt-auto pt-3">
                            <span class="text-lg font-black tracking-tight text-black">${item.price}</span>
                            <div class="flex items-center gap-1.5" title="${item.stock}">
                                <div class="w-1.5 h-1.5 rounded-none ${stockDot}"></div>
                                <span class="text-[9px] font-bold uppercase ${stockText} hidden sm:inline-block truncate max-w-[50px]">${isOutOfStock?'OUT':'IN'}</span>
                            </div>
                        </div>
                    </div>
                </a>
                `;
            }).join('');
        }

        // Filtering Logic
        function applyFilters() {
            const selectedCategories = Array.from(document.querySelectorAll('.filter-category:checked')).map(cb => cb.value);
            const selectedPrices = Array.from(document.querySelectorAll('.filter-price:checked')).map(cb => cb.value);
            const inStockOnly = document.querySelector('.filter-stock:checked') !== null;

            let filtered = allProducts;

            // Category Filter
            if (selectedCategories.length > 0) {
                filtered = filtered.filter(p => selectedCategories.includes(p.category));
            }

            // In Stock Filter
            if (inStockOnly) {
                filtered = filtered.filter(p => !p.stock.toLowerCase().includes('out') && !p.stock.toLowerCase().includes('sold'));
            }

            // Price Filter
            if (selectedPrices.length > 0) {
                filtered = filtered.filter(p => {
                    const priceNum = p.priceNum;
                    if (priceNum === null) return false;
                    
                    return selectedPrices.some(range => {
                        if (range === 'under-500') return priceNum < 500;
                        if (range === '500-1000') return priceNum >= 500 && priceNum <= 1000;
                        if (range === 'over-1000') return priceNum > 1000;
                        return false;
                    });
                });
            }

            renderGrid(filtered);
        }

        // Initialization
        document.addEventListener('DOMContentLoaded', () => {
            fetch('../scripts/live_inventory.json')
                .then(r => r.json())
                .then(data => {
                    // Filter just for this brand immediately!
                    // This dynamically handles Garrett, Minelab, XP, Nokta based on the brand var we'll inject via Regex from Python
                    allProducts = data.filter(item => 
                        ('{brand_name}'.includes('Nokta') ? item.brand.includes('Nokta') : item.brand.toLowerCase() === '{brand_name}'.toLowerCase()) 
                        && !isBundleItem(item)
                    ).map(item => ({
                        ...item,
                        category: getCategory(item),
                        priceNum: extractPrice(item.price)
                    }));
                    
                    loading.style.display = 'none';

                    // Initial Render
                    applyFilters();

                    // Attach Event Listeners to checkboxes
                    document.querySelectorAll('.filter-checkbox').forEach(cb => {
                        cb.addEventListener('change', applyFilters);
                    });

                    // Clear Filters functionality
                    document.getElementById('clear-filters').addEventListener('click', () => {
                        document.querySelectorAll('.filter-checkbox').forEach(cb => cb.checked = false);
                        applyFilters();
                    });
                })
                .catch(err => {
                    console.error("Failed to load inventory:", err);
                    loading.innerHTML = '<p class="text-red-500 font-bold uppercase tracking-widest text-sm">Failed to load inventory. Please try again later.</p>';
                });
        });
    </script>"""

CSS_STYLES = """    <style>
        .custom-scrollbar::-webkit-scrollbar {
            width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: #f1f1f1; 
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #d1d5db; 
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: #9ca3af; 
        }

        /* Checkbox Styling */
        .filter-checkbox {
            appearance: none;
            width: 1rem;
            height: 1rem;
            border: 1px solid #d1d5db;
            border-radius: 0;
            outline: none;
            cursor: pointer;
            position: relative;
            transition: all 0.2s ease;
        }
        
        .filter-checkbox:checked {
            background-color: #000;
            border-color: #000;
        }

        .filter-checkbox:checked::after {
            content: '';
            position: absolute;
            left: 4px;
            top: 1px;
            width: 4px;
            height: 8px;
            border: solid white;
            border-width: 0 2px 2px 0;
            transform: rotate(45deg);
        }
        
        /* Grid product card styling */
        .product-card {
            background: #fff;
            border: 1px solid #e5e7eb;
            transition: box-shadow 0.2s ease, border-color 0.2s ease;
            position: relative;
            display: flex;
            flex-direction: column;
        }
        
        .product-card:hover {
            border-color: #000;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
            z-index: 10;
        }

        .img-container {
            width: 100%;
            aspect-ratio: 1 / 1;
            padding: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: #fff;
        }

        .img-container img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
        
        .textContainer {
            padding: 1rem;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }
    </style>"""

for filename, brand_name in targets.items():
    path = os.path.join(pages_dir, filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Inject CSS inside <head> if not exists
        if '.filter-checkbox' not in content:
            content = content.replace("</head>", f"{CSS_STYLES}\n</head>")
            
        # 2. Extract out from <!-- Category Filter Bar --> down to <!-- Footer -->
        # We want to replace the old grid mechanism with the new Sidebar+Grid
        pattern = re.compile(r'<!-- Category Filter Bar -->.*?<!-- Footer -->', re.DOTALL)
        
        brand_sidebar = SIDEBAR_HTML.replace('{brand}', brand_name)
        new_body = brand_sidebar + '\n    <!-- Footer -->'
        
        content = pattern.sub(new_body, content)
        
        # 3. Replace <script> blocks governing the grid
        script_pattern = re.compile(r'<script>\s*// === BUNDLE EXCLUSION.*?</script>', re.DOTALL)
        brand_script = NEW_SCRIPT.replace('{brand_name}', brand_name)
        
        content = script_pattern.sub(brand_script, content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Patched {filename} successfully for {brand_name}")
