import os
from pathlib import Path

pages_dir = Path(r"c:\Projects\Gateway_Final\pages")
targets = ["garrett.html", "minelab.html", "nokta.html", "xp.html"]

OLD_BLOCK = """                        <div class="product-card border border-gray-200 shadow-xl p-10 flex flex-col items-center justify-between text-center transition-transform hover:-translate-y-2 bg-white rounded-none" data-category="${cat}">
                            <div class="h-64 w-full bg-white mb-8 flex items-center justify-center p-4">
                                ${item.image ? `<img src="${item.image}" alt="${item.name}" class="max-h-full max-w-full object-contain">` : '<div class="text-gray-300 font-bold uppercase tracking-widest text-sm border-2 border-dashed border-gray-200 w-full h-full flex items-center justify-center bg-gray-50">No Image</div>'}
                            </div>
                            <h3 class="text-3xl font-black text-black mb-6 uppercase tracking-tight leading-tight px-4">${item.name}</h3>
                            <div class="${item.stock === 'In Stock' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'} px-6 py-3 font-bold uppercase tracking-widest text-sm w-full mb-8">
                                ${item.stock}
                            </div>
                            <a href="mailto:info@gatewaydetectors.com?subject=Inquiry%20About%20${encodeURIComponent(item.name)}" class="mt-auto bg-black text-white px-10 py-5 font-black uppercase tracking-widest text-lg w-full hover:bg-gray-800 transition block">Contact Us</a>
                        </div>"""

NEW_BLOCK = """                        <a href="product.html?id=${item.slug}" class="product-card cursor-pointer block border border-gray-200 shadow-xl p-10 flex flex-col items-center justify-between text-center transition-transform hover:-translate-y-2 bg-white rounded-none" data-category="${cat}">
                            <div class="h-64 w-full bg-white mb-8 flex items-center justify-center p-4">
                                ${item.image ? `<img src="${item.image}" alt="${item.name}" class="max-h-full max-w-full object-contain">` : '<div class="text-gray-300 font-bold uppercase tracking-widest text-sm border-2 border-dashed border-gray-200 w-full h-full flex items-center justify-center bg-gray-50">No Image</div>'}
                            </div>
                            <h3 class="text-3xl font-black text-black mb-6 uppercase tracking-tight leading-tight px-4">${item.name}</h3>
                            <div class="${item.stock === 'In Stock' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'} px-6 py-3 font-bold uppercase tracking-widest text-sm w-full mb-8">
                                ${item.stock}
                            </div>
                            <div class="mt-auto bg-black text-white px-10 py-5 font-black uppercase tracking-widest text-lg w-full hover:bg-gray-800 transition flex items-center justify-center gap-2">
                                <span>View Details</span>
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                            </div>
                        </a>"""

for t in targets:
    p = pages_dir / t
    if p.exists():
        content = p.read_text(encoding="utf-8")
        if OLD_BLOCK in content:
            new_content = content.replace(OLD_BLOCK, NEW_BLOCK)
            p.write_text(new_content, encoding="utf-8")
            print(f"Updated {t}")
        else:
            print(f"Could not find exact block in {t}")
    else:
        print(f"File not found: {t}")
