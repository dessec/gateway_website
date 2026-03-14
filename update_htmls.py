import os
from pathlib import Path

def update_root_index():
    f = Path('index.html')
    if not f.exists(): return
    text = f.read_text(encoding='utf-8')
    
    # Nav bar replacement
    old_nav = """        <div class="hidden lg:flex items-center space-x-6">
            <a href="index.html" class="nav-link active">Home</a>
            <span class="text-gray-300">-</span>
            <a href="shop.html" class="nav-link">Shop</a>
            <span class="text-gray-300">-</span>
            <a href="about.html" class="nav-link">About Us</a>
            <span class="text-gray-300">-</span>
            <a href="accessories.html" class="nav-link">Tools</a>
            <span class="text-gray-300">-</span>
            <a href="pages/community-map.html" class="nav-link">Maps</a>
            <span class="text-gray-300">-</span>
            <a href="cart.html" class="nav-link">Cart</a>
        </div>"""
    new_nav = """        <div class="hidden lg:flex items-center space-x-6">
            <a href="index.html" class="nav-link active">Home</a>
            <span class="text-gray-300">-</span>
            <a href="#brands" class="nav-link">Shop</a>
            <span class="text-gray-300">-</span>
            <a href="#about" class="nav-link">About Us</a>
            <span class="text-gray-300">-</span>
            <a href="#tools" class="nav-link">Tools</a>
            <span class="text-gray-300">-</span>
            <a href="pages/community-map.html" class="nav-link">Maps</a>
            <span class="text-gray-300">-</span>
            <a href="#contact" class="nav-link">Contact</a>
        </div>"""
    text = text.replace(old_nav, new_nav)
    
    # Add IDs for anchors
    text = text.replace('<section class="w-full max-w-[1280px] mx-auto px-6 py-12">', '<section id="tools" class="w-full max-w-[1280px] mx-auto px-6 py-12">')
    text = text.replace('<section class="max-w-[1280px] mx-auto px-6 pb-20 w-full relative">', '<section id="brands" class="max-w-[1280px] mx-auto px-6 pb-20 w-full relative">')
    text = text.replace('<footer class="bg-[#050505] text-white pt-24 pb-16 w-full">', '<footer id="about" class="bg-[#050505] text-white pt-24 pb-16 w-full">')
    text = text.replace('<div class="text-[13px] font-semibold text-gray-400 flex flex-col">', '<div id="contact" class="text-[13px] font-semibold text-gray-400 flex flex-col">')
    
    # Fix the footer quick links
    old_footer_links = """                    <li><a href="index.html" class="hover:text-white transition cursor-pointer inline-block">Home</a>
                    </li>
                    <li><a href="shop.html" class="hover:text-white transition cursor-pointer inline-block">Shop</a>
                    </li>
                    <li><a href="about.html" class="hover:text-white transition cursor-pointer inline-block">About
                            Us</a></li>
                    <li><a href="accessories.html"
                            class="hover:text-white transition cursor-pointer inline-block">Tools</a></li>
                    <li><a href="pages/community-map.html"
                            class="hover:text-white transition cursor-pointer inline-block">Maps</a></li>
                    <li><a href="cart.html" class="hover:text-white transition cursor-pointer inline-block">Cart</a>
                    </li>"""
    new_footer_links = """                    <li><a href="index.html" class="hover:text-white transition cursor-pointer inline-block">Home</a>
                    </li>
                    <li><a href="#brands" class="hover:text-white transition cursor-pointer inline-block">Shop</a>
                    </li>
                    <li><a href="#about" class="hover:text-white transition cursor-pointer inline-block">About
                            Us</a></li>
                    <li><a href="#tools"
                            class="hover:text-white transition cursor-pointer inline-block">Tools</a></li>
                    <li><a href="pages/community-map.html"
                            class="hover:text-white transition cursor-pointer inline-block">Maps</a></li>
                    <li><a href="#contact" class="hover:text-white transition cursor-pointer inline-block">Contact</a>
                    </li>"""
    text = text.replace(old_footer_links, new_footer_links)

    f.write_text(text, encoding='utf-8')

def update_pages():
    for f in Path('pages').glob('*.html'):
        text = f.read_text(encoding='utf-8')
        
        # Nav bar replacement
        old_nav = """        <div class="hidden lg:flex items-center space-x-6">
            <a href="../index.html" class="nav-link">Home</a>
            <span class="text-gray-300">-</span>
            <a href="shop.html" class="nav-link active">Shop</a>
            <span class="text-gray-300">-</span>
            <a href="about.html" class="nav-link">About Us</a>
            <span class="text-gray-300">-</span>
            <a href="accessories.html" class="nav-link">Tools</a>
            <span class="text-gray-300">-</span>
            <a href="community-map.html" class="nav-link">Maps</a>
            <span class="text-gray-300">-</span>
            <a href="cart.html" class="nav-link">Cart</a>
        </div>"""
        
        old_nav2 = """        <div class="hidden lg:flex items-center space-x-6">
            <a href="../index.html" class="nav-link">Home</a>
            <span class="text-gray-300">-</span>
            <a href="shop.html" class="nav-link">Shop</a>
            <span class="text-gray-300">-</span>
            <a href="about.html" class="nav-link">About Us</a>
            <span class="text-gray-300">-</span>
            <a href="accessories.html" class="nav-link">Tools</a>
            <span class="text-gray-300">-</span>
            <a href="community-map.html" class="nav-link active">Maps</a>
            <span class="text-gray-300">-</span>
            <a href="cart.html" class="nav-link">Cart</a>
        </div>"""
        
        new_nav = """        <div class="hidden lg:flex items-center space-x-6">
            <a href="../index.html" class="nav-link">Home</a>
            <span class="text-gray-300">-</span>
            <a href="#inventory-grid" class="nav-link active">Shop</a>
            <span class="text-gray-300">-</span>
            <a href="../index.html#about" class="nav-link">About Us</a>
            <span class="text-gray-300">-</span>
            <a href="../index.html#tools" class="nav-link">Tools</a>
            <span class="text-gray-300">-</span>
            <a href="community-map.html" class="nav-link">Maps</a>
            <span class="text-gray-300">-</span>
            <a href="../index.html#contact" class="nav-link">Contact</a>
        </div>"""
        
        if 'community-map' in f.name:
            new_nav = new_nav.replace('class="nav-link active">Shop', 'class="nav-link">Shop').replace('class="nav-link">Maps', 'class="nav-link active">Maps')
            text = text.replace(old_nav2, new_nav)
        else:
            text = text.replace(old_nav, new_nav)

        # Card content replacement (remove price, add email link)
        if 'community-map' not in f.name and 'community-clubs' not in f.name:
            old_card = """<p class="text-[2.5rem] font-bold text-gray-900 mb-8 tracking-tighter">${item.price}</p>
                            <div class="${item.stock === 'In Stock' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'} px-6 py-3 font-bold uppercase tracking-widest text-sm w-full mb-8">
                                ${item.stock}
                            </div>
                            <a href="${item.url}" target="_blank" class="mt-auto bg-black text-white px-10 py-5 font-black uppercase tracking-widest text-lg w-full hover:bg-gray-800 transition block">Verify on Radioworld</a>"""
            
            new_card = """<div class="${item.stock === 'In Stock' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'} px-6 py-3 font-bold uppercase tracking-widest text-sm w-full mb-8">
                                ${item.stock}
                            </div>
                            <a href="mailto:info@gatewaydetectors.com?subject=Inquiry%20About%20${encodeURIComponent(item.name)}" class="mt-auto bg-black text-white px-10 py-5 font-black uppercase tracking-widest text-lg w-full hover:bg-gray-800 transition block">Contact Us</a>"""
            
            text = text.replace(old_card, new_card)
        
        # Footer Quick Links
        old_footer_links = """                    <li><a href="../index.html" class="hover:text-white transition cursor-pointer inline-block">Home</a>
                    </li>
                    <li><a href="shop.html" class="hover:text-white transition cursor-pointer inline-block">Shop</a>
                    </li>
                    <li><a href="about.html" class="hover:text-white transition cursor-pointer inline-block">About
                            Us</a></li>
                    <li><a href="accessories.html"
                            class="hover:text-white transition cursor-pointer inline-block">Tools</a></li>
                    <li><a href="community-map.html"
                            class="hover:text-white transition cursor-pointer inline-block">Maps</a></li>
                    <li><a href="cart.html" class="hover:text-white transition cursor-pointer inline-block">Cart</a>
                    </li>"""
        new_footer_links = """                    <li><a href="../index.html" class="hover:text-white transition cursor-pointer inline-block">Home</a>
                    </li>
                    <li><a href="#inventory-grid" class="hover:text-white transition cursor-pointer inline-block">Shop</a>
                    </li>
                    <li><a href="../index.html#about" class="hover:text-white transition cursor-pointer inline-block">About
                            Us</a></li>
                    <li><a href="../index.html#tools"
                            class="hover:text-white transition cursor-pointer inline-block">Tools</a></li>
                    <li><a href="community-map.html"
                            class="hover:text-white transition cursor-pointer inline-block">Maps</a></li>
                    <li><a href="../index.html#contact" class="hover:text-white transition cursor-pointer inline-block">Contact</a>
                    </li>"""
        text = text.replace(old_footer_links, new_footer_links)

        f.write_text(text, encoding='utf-8')

if __name__ == '__main__':
    update_root_index()
    update_pages()
    print("HTML Update Complete")
