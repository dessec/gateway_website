/* ============================================================
   gateway-auth.js
   Global Supabase client, cart engine, and auth navbar renderer
   ============================================================ */

(function () {
    'use strict';

    // ── Supabase Client Initialization ──────────────────────────
    const SUPABASE_URL = 'https://qoziwcymmrvsunrwsdlt.supabase.co';
    const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFveml3Y3ltbXJ2c3VucndzZGx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc5NzY1ODIsImV4cCI6MjEwMzU1MjU4Mn0.-dzHZlKuAKNlPhhYIZxhq8ifIfwOXBOHteaSBYapMLg';

    let supabaseClient = null;
    try {
        if (typeof supabase !== 'undefined' && supabase.createClient) {
            supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        }
    } catch (e) {
        console.warn('[Gateway Auth] Supabase SDK not loaded:', e);
    }
    window._supabase = supabaseClient;

    // ── LocalStorage Cart Engine ────────────────────────────────
    const CART_KEY = 'gateway_cart';

    function getCart() {
        try {
            return JSON.parse(localStorage.getItem(CART_KEY)) || [];
        } catch { return []; }
    }

    function saveCart(cart) {
        localStorage.setItem(CART_KEY, JSON.stringify(cart));
        window.dispatchEvent(new CustomEvent('cart-updated', { detail: { count: cart.length } }));
        updateCartBadge();
    }

    function addToCart(item) {
        const cart = getCart();
        const existing = cart.find(c => c.slug === item.slug);
        if (existing) {
            existing.qty = (existing.qty || 1) + 1;
        } else {
            cart.push({ ...item, qty: 1 });
        }
        saveCart(cart);
        showAddedToast(item.name || 'Item');
    }

    function removeFromCart(slug) {
        const cart = getCart().filter(c => c.slug !== slug);
        saveCart(cart);
    }

    function updateCartQty(slug, qty) {
        const cart = getCart();
        const item = cart.find(c => c.slug === slug);
        if (item) {
            item.qty = Math.max(1, qty);
            saveCart(cart);
        }
    }

    function getCartCount() {
        return getCart().reduce((sum, item) => sum + (item.qty || 1), 0);
    }

    function clearCart() {
        localStorage.removeItem(CART_KEY);
        window.dispatchEvent(new CustomEvent('cart-updated', { detail: { count: 0 } }));
        updateCartBadge();
    }

    // ── Expose cart API globally ────────────────────────────────
    window.GatewayCart = { getCart, addToCart, removeFromCart, updateCartQty, getCartCount, clearCart, saveCart };

    // ── Toast Notification ──────────────────────────────────────
    function showAddedToast(name) {
        const toast = document.createElement('div');
        toast.className = 'fixed bottom-6 right-6 z-[9999] bg-gray-900 text-white px-5 py-3 rounded-lg shadow-2xl flex items-center gap-3 transform translate-y-4 opacity-0 transition-all duration-300';
        toast.innerHTML = `
            <svg class="w-5 h-5 text-green-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            <div>
                <p class="text-xs font-bold uppercase tracking-wider text-green-400">Added to Reserve List</p>
                <p class="text-sm font-semibold text-gray-200 mt-0.5">${name}</p>
            </div>
        `;
        document.body.appendChild(toast);
        requestAnimationFrame(() => {
            toast.style.transform = 'translateY(0)';
            toast.style.opacity = '1';
        });
        setTimeout(() => {
            toast.style.transform = 'translateY(4px)';
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 2500);
    }

    // ── Cart Badge Update ───────────────────────────────────────
    function updateCartBadge() {
        const badge = document.getElementById('cart-badge');
        if (!badge) return;
        const count = getCartCount();
        badge.textContent = count;
        badge.style.display = count > 0 ? 'flex' : 'none';
    }

    // ── Auth + Cart Navbar Renderer ─────────────────────────────
    function renderAuthUI(container) {
        if (!container) return;

        async function render() {
            let session = null;
            if (supabaseClient) {
                try {
                    const { data } = await supabaseClient.auth.getSession();
                    session = data?.session;
                } catch (e) {
                    console.warn('[Gateway Auth] getSession error:', e);
                }
            }

            if (session) {
                renderLoggedIn(container, session);
            } else {
                renderLoggedOut(container);
            }
        }

        render();

        // Listen for auth changes
        if (supabaseClient) {
            supabaseClient.auth.onAuthStateChange((_event, session) => {
                if (session) {
                    renderLoggedIn(container, session);
                } else {
                    renderLoggedOut(container);
                }
            });
        }
    }

    function renderLoggedOut(container) {
        container.innerHTML = `
            <div class="flex items-center gap-4">
                <button id="nav-signin-btn" class="text-sm font-bold text-gray-600 hover:text-amber-600 transition-colors uppercase tracking-wider cursor-pointer">Sign In</button>
                <button id="nav-signup-btn" class="text-sm font-bold bg-amber-600 text-white px-4 py-2 rounded hover:bg-amber-700 transition-colors uppercase tracking-wider cursor-pointer shadow-sm">Sign Up</button>
                <a href="${getPagePrefix()}checkout.html" class="relative group cursor-pointer" title="Reserve Cart">
                    <svg class="w-6 h-6 text-gray-500 group-hover:text-amber-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>
                    <span id="cart-badge" class="absolute -top-2 -right-2 bg-red-500 text-white text-[10px] font-black w-5 h-5 rounded-full items-center justify-center shadow-sm" style="display:none;">0</span>
                </a>
            </div>
        `;

        document.getElementById('nav-signin-btn')?.addEventListener('click', () => {
            if (window.GatewayAuthModal) window.GatewayAuthModal.open('signin');
        });
        document.getElementById('nav-signup-btn')?.addEventListener('click', () => {
            if (window.GatewayAuthModal) window.GatewayAuthModal.open('signup');
        });

        updateCartBadge();
    }

    function renderLoggedIn(container, session) {
        const user = session.user;
        const avatarUrl = user?.user_metadata?.avatar_url || user?.user_metadata?.picture || '';
        const initials = (user?.email || 'U')[0].toUpperCase();

        container.innerHTML = `
            <div class="flex items-center gap-4">
                <a href="${getPagePrefix()}checkout.html" class="relative group cursor-pointer" title="Reserve Cart">
                    <svg class="w-6 h-6 text-gray-500 group-hover:text-amber-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>
                    <span id="cart-badge" class="absolute -top-2 -right-2 bg-red-500 text-white text-[10px] font-black w-5 h-5 rounded-full items-center justify-center shadow-sm" style="display:none;">0</span>
                </a>
                <div class="relative">
                    <button id="avatar-btn" class="w-10 h-10 rounded-full overflow-hidden border-2 border-gray-200 hover:border-amber-500 transition-colors cursor-pointer shadow-sm flex items-center justify-center bg-amber-600 text-white font-bold text-sm" title="Account">
                        ${avatarUrl ? `<img src="${avatarUrl}" alt="Avatar" class="w-full h-full object-cover">` : initials}
                    </button>
                    <div id="avatar-dropdown" class="hidden absolute right-0 top-full mt-2 w-56 bg-white border border-gray-200 rounded-xl shadow-xl z-[100] overflow-hidden transform origin-top-right scale-95 opacity-0 transition-all duration-200">
                        <div class="px-4 py-3 border-b border-gray-100 bg-gray-50">
                            <p class="text-xs font-bold text-gray-900 truncate">${user?.email || 'User'}</p>
                            <p class="text-[10px] text-amber-600 font-bold uppercase tracking-wider mt-0.5">Gateway Member</p>
                        </div>
                        <a href="${getPagePrefix()}profile.html" class="flex items-center gap-3 px-4 py-3 text-sm font-semibold text-gray-700 hover:bg-amber-50 hover:text-amber-700 transition-colors">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                            My Profile
                        </a>
                        <a href="${getPagePrefix()}checkout.html" class="flex items-center gap-3 px-4 py-3 text-sm font-semibold text-gray-700 hover:bg-amber-50 hover:text-amber-700 transition-colors">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 100 4 2 2 0 000-4z"/></svg>
                            My Reserve Cart
                        </a>
                        <button id="signout-btn" class="w-full flex items-center gap-3 px-4 py-3 text-sm font-semibold text-red-600 hover:bg-red-50 transition-colors border-t border-gray-100">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/></svg>
                            Sign Out
                        </button>
                    </div>
                </div>
            </div>
        `;

        // Dropdown toggle
        const avatarBtn = document.getElementById('avatar-btn');
        const dropdown = document.getElementById('avatar-dropdown');
        if (avatarBtn && dropdown) {
            avatarBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const isHidden = dropdown.classList.contains('hidden');
                dropdown.classList.toggle('hidden', !isHidden);
                setTimeout(() => {
                    dropdown.style.opacity = isHidden ? '1' : '0';
                    dropdown.style.transform = isHidden ? 'scale(1)' : 'scale(0.95)';
                }, 10);
            });
            document.addEventListener('click', () => {
                dropdown.classList.add('hidden');
                dropdown.style.opacity = '0';
                dropdown.style.transform = 'scale(0.95)';
            });
        }

        // Sign out
        document.getElementById('signout-btn')?.addEventListener('click', async () => {
            if (supabaseClient) {
                await supabaseClient.auth.signOut();
            }
        });

        updateCartBadge();
    }

    // ── Page prefix helper (handles root vs pages/ depth) ───────
    function getPagePrefix() {
        const path = window.location.pathname;
        if (path.includes('/pages/')) return '';
        return 'pages/';
    }

    // ── Auto-init on DOMContentLoaded ───────────────────────────
    document.addEventListener('DOMContentLoaded', () => {
        const container = document.getElementById('auth-cart-container');
        if (container) renderAuthUI(container);
    });

    // Listen for cart updates from other tabs/components
    window.addEventListener('cart-updated', () => updateCartBadge());

})();
