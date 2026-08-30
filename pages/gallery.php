<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gallery - Gateway Metal Detectors</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f9fafb; color: #111827; }
        .nav-link {
            position: relative;
            display: inline-block;
            padding-bottom: 2px;
            color: #374151;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.95rem;
            letter-spacing: 0.06em;
            transition: color 0.3s ease;
        }

        .nav-link:hover, .nav-link.active {
            color: #111827;
        }

        .nav-link::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            bottom: -4px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #d97706;
            transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .nav-link:hover::after, .nav-link.active::after {
            width: 100%;
        }
    </style>
</head>

<body class="bg-[#f9fafb] text-gray-900 w-full overflow-x-hidden flex flex-col min-h-screen selection:bg-amber-600 selection:text-white">

    <!-- Header Navigation -->
    <nav class="fixed top-0 left-0 right-0 h-20 bg-white/95 backdrop-blur-md border-b border-gray-200 shadow-sm z-50 flex items-center justify-between px-6 md:px-12 w-full">
        <!-- Logo -->
        <a href="../index.html" class="flex items-center gap-3 group transition cursor-pointer">
            <img src="../assets/images/gateway_medallion.png" alt="Gateway Medallion" class="h-16 w-auto object-contain drop-shadow-md group-hover:scale-105 transition-transform duration-300">
            <div class="flex flex-col justify-center">
                <span class="text-xl font-black tracking-[0.16em] uppercase text-gray-900 leading-tight group-hover:text-amber-600 transition-colors">GATEWAY</span>
                <span class="text-[0.58rem] tracking-[0.28em] font-bold uppercase text-amber-600">Metal Detectors</span>
            </div>
        </a>

        <!-- Center Nav Links -->
        <div class="hidden lg:flex items-center space-x-6 absolute left-1/2 -translate-x-1/2">
            <a href="../index.html" class="nav-link">Home</a>
            <span class="text-gray-300">-</span>
            <a href="shop.html" class="nav-link">Shop</a>
            <span class="text-gray-300">-</span>
            <a href="about.html" class="nav-link">About Us</a>
            <span class="text-gray-300">-</span>
            <a href="events.html" class="nav-link">Events</a>
            <span class="text-gray-300">-</span>
            <a href="community-map.html" class="nav-link">Maps</a>
            <span class="text-gray-300">-</span>
            <a href="gallery.php" class="nav-link active">Gallery</a>
            <span class="text-gray-300">-</span>
            <a href="contact.html" class="nav-link">Contact</a>
        </div>
        <div id="auth-cart-container" class="hidden lg:flex items-center"></div>
    </nav>
    <div class="h-20 w-full"></div>

    <!-- Main Content: Photo Gallery -->
    <main class="w-full max-w-[1280px] mx-auto px-6 py-20 flex-grow flex flex-col items-center text-center">
        <p class="text-[10px] font-black uppercase tracking-[0.35em] text-amber-600 mb-6">Historical Archives</p>
        <h1 class="text-4xl md:text-6xl font-black text-gray-900 leading-none mb-10 tracking-tight" style="font-family: Georgia, serif;">
            Photo Gallery
        </h1>
        <div class="h-[3px] w-16 bg-amber-600 mb-12"></div>
        <div class="w-full columns-1 sm:columns-2 md:columns-3 lg:columns-4 gap-6 space-y-6">
            <?php
            $dir = "../assets/images/gallery/";
            if (is_dir($dir)) {
                $images = glob($dir . "*.{jpg,jpeg,png,gif,JPG,JPEG,PNG,GIF}", GLOB_BRACE);
                foreach($images as $image) {
                    echo '<div class="break-inside-avoid overflow-hidden rounded-xl shadow-md cursor-pointer relative group">';
                    echo '  <img src="' . htmlspecialchars($image) . '" loading="lazy" alt="Gateway Metal Detectors Discovery" class="w-full transform group-hover:scale-105 transition-all duration-500 ease-out">';
                    echo '  <div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-300"></div>';
                    echo '</div>';
                }
            } else {
                echo '<p>Gallery images not found.</p>';
            }
            ?>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 text-gray-800 pt-24 pb-16 w-full mt-auto">
        <div class="max-w-[1280px] mx-auto px-6 w-full grid grid-cols-1 md:grid-cols-4 gap-12 text-left">
            <div class="col-span-1 md:col-span-2 md:pr-16">
                <a href="../index.html" class="flex items-center gap-3 group transition cursor-pointer mb-6">
                    <img src="../assets/images/gateway_medallion.png" alt="Gateway Medallion" class="h-11 w-auto object-contain drop-shadow-md group-hover:scale-105 transition-transform duration-300">
                    <div class="flex flex-col justify-center">
                        <span class="text-2xl font-black tracking-[0.16em] uppercase text-gray-900 leading-tight group-hover:text-amber-600 transition-colors">GATEWAY</span>
                        <span class="text-[0.58rem] tracking-[0.28em] font-bold uppercase text-amber-600">Metal Detectors</span>
                    </div>
                </a>
                <p class="text-xs text-gray-600 font-semibold leading-relaxed mb-8">
                    <span class="text-gray-900 font-bold">ABOUT US:</span> Gateway Metal Detectors is Hamilton's dedicated treasure hunting hub, founded on a lifelong passion for discovery. We carry professional-grade equipment from the world's leading brands — Nokta, Minelab, XP, and Garrett. Whether you're a first-time hobbyist or a seasoned detectorist, we have the gear and the knowledge to back it up. Serving Southern Ontario and shipping across Canada and worldwide.
                </p>
                <p class="text-[10px] text-gray-500 font-semibold">&copy; 2026 Gateway Metal Detectors. All Rights Reserved.</p>
            </div>
            <div>
                <ul class="space-y-3 pt-1 text-xs font-semibold text-gray-600 uppercase tracking-widest flex flex-col items-start">
                    <li><a href="../index.html" class="hover:text-gray-900 transition cursor-pointer inline-block">Home</a></li>
                    <li><a href="shop.html" class="hover:text-gray-900 transition cursor-pointer inline-block">Shop</a></li>
                    <li><a href="about.html" class="hover:text-gray-900 transition cursor-pointer inline-block">About Us</a></li>
                    <li><a href="events.html" class="hover:text-gray-900 transition cursor-pointer inline-block">Events</a></li>
                    <li><a href="community-map.html" class="hover:text-gray-900 transition cursor-pointer inline-block">Maps</a></li>
                    <li><a href="gallery.php" class="hover:text-gray-900 transition cursor-pointer inline-block">Gallery</a></li>
                    <li><a href="contact.html" class="hover:text-gray-900 transition cursor-pointer inline-block">Contact</a></li>
                </ul>
            </div>
            <div class="text-[13px] font-semibold text-gray-600 flex flex-col">
                <h4 class="text-gray-900 font-bold mb-5 tracking-wider uppercase text-xs text-amber-600">Contact info</h4>
                <p class="mb-3 flex items-start"><span class="w-5 shrink-0 inline-block text-amber-600">📞</span> +1(905)870-8689</p>
                <p class="mb-3 flex items-start"><span class="w-5 shrink-0 inline-block text-amber-600">📍</span> Hamilton, Ontario, Canada.</p>
                <p class="mb-8 flex items-start"><span class="w-5 shrink-0 inline-block text-amber-600">✉️</span> gatewaydetecting@hotmail.com</p>
            </div>
        </div>
    
        <!-- Regional Service Area (Low Profile SEO Block) -->
        <div class="max-w-[1280px] mx-auto px-6 pt-12 mt-12 border-t border-gray-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 text-[11px] text-gray-500 font-medium">
            <span class="text-gray-700 font-bold uppercase tracking-wider text-[10px] text-amber-600">Proudly Serving Southern Ontario:</span>
            <div class="flex flex-wrap gap-x-2 gap-y-1 text-gray-500">
                <span>Hamilton</span> • <span>Stoney Creek</span> • <span>Ancaster</span> • <span>Burlington</span> • <span>Oakville</span> • <span>Mississauga</span> • <span>Toronto</span>
            </div>
        </div>
    </footer>
<script src="../scripts/gateway-auth.js"></script>
<script src="../scripts/auth-modal.js"></script>
<script type='text/javascript' data-cfasync='false'>window.purechatApi = { l: [], t: [], on: function () { this.l.push(arguments); } }; (function () { var done = false; var script = document.createElement('script'); script.async = true; script.type = 'text/javascript'; script.src = 'https://app.purechat.com/VisitorWidget/WidgetScript'; document.getElementsByTagName('HEAD').item(0).appendChild(script); script.onreadystatechange = script.onload = function (e) { if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete')) { var w = new PCWidget({c: '76adb4c9-78ac-4ea9-b7b3-36e4412eca7d', f: true }); done = true; } }; })();</script>
</body>
</html>
