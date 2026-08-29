/* ============================================================
   auth-modal.js
   Beautiful animated auth modal with email/password, OAuth,
   and community compliance checkbox
   ============================================================ */

(function () {
    'use strict';

    let modalEl = null;

    function buildModal() {
        if (modalEl) return modalEl;

        modalEl = document.createElement('div');
        modalEl.id = 'auth-modal-overlay';
        modalEl.className = 'fixed inset-0 z-[9998] hidden';
        modalEl.innerHTML = `
            <!-- Backdrop -->
            <div id="auth-backdrop" class="absolute inset-0 bg-black/60 backdrop-blur-sm opacity-0 transition-opacity duration-300"></div>

            <!-- Modal Card -->
            <div class="absolute inset-0 flex items-center justify-center p-4">
                <div id="auth-card" class="relative bg-white rounded-2xl shadow-2xl border border-gray-200 w-full max-w-md overflow-hidden transform scale-95 opacity-0 transition-all duration-300">
                    
                    <!-- Close Button -->
                    <button id="auth-close-btn" class="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full bg-gray-100 hover:bg-gray-200 transition-colors z-10">
                        <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                    </button>

                    <!-- Header -->
                    <div class="px-8 pt-8 pb-4 text-center">
                        <div class="flex items-center justify-center gap-2 mb-3">
                            <span class="text-xl font-black tracking-[0.16em] uppercase text-gray-900">GATEWAY</span>
                        </div>
                        <p class="text-[10px] font-black uppercase tracking-[0.3em] text-amber-600">Metal Detectors Community</p>
                    </div>

                    <!-- Tab Switcher -->
                    <div class="flex border-b border-gray-200 mx-8">
                        <button id="tab-signin" class="flex-1 py-3 text-xs font-black uppercase tracking-widest text-amber-600 border-b-2 border-amber-600 transition-all">Sign In</button>
                        <button id="tab-signup" class="flex-1 py-3 text-xs font-black uppercase tracking-widest text-gray-400 border-b-2 border-transparent hover:text-gray-600 transition-all">Sign Up</button>
                    </div>

                    <!-- Forms Container -->
                    <div class="px-8 py-6">

                        <!-- Sign In Form -->
                        <form id="signin-form" class="space-y-4">
                            <div>
                                <label class="block text-[10px] font-bold uppercase tracking-widest text-gray-700 mb-2">Email Address</label>
                                <input type="email" id="signin-email" required class="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-colors" placeholder="you@example.com">
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold uppercase tracking-widest text-gray-700 mb-2">Password</label>
                                <input type="password" id="signin-password" required class="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-colors" placeholder="••••••••">
                            </div>
                            <div id="signin-error" class="hidden text-red-500 text-xs font-bold bg-red-50 border border-red-200 rounded-lg px-4 py-2"></div>
                            <button type="submit" id="signin-submit" class="w-full bg-amber-600 text-white font-black uppercase tracking-widest text-xs py-4 rounded-lg hover:bg-amber-700 transition-colors shadow-md">Sign In</button>
                        </form>

                        <!-- Sign Up Form -->
                        <form id="signup-form" class="space-y-4 hidden">
                            <div>
                                <label class="block text-[10px] font-bold uppercase tracking-widest text-gray-700 mb-2">Email Address</label>
                                <input type="email" id="signup-email" required class="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-colors" placeholder="you@example.com">
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold uppercase tracking-widest text-gray-700 mb-2">Password</label>
                                <input type="password" id="signup-password" required minlength="6" class="w-full bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-sm text-gray-900 placeholder:text-gray-400 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none transition-colors" placeholder="Min. 6 characters">
                            </div>

                            <!-- Community ToS Compliance Checkbox -->
                            <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                                <label class="flex items-start gap-3 cursor-pointer group">
                                    <input type="checkbox" id="tos-checkbox" class="mt-1 w-4 h-4 accent-amber-600 cursor-pointer shrink-0">
                                    <span class="text-[11px] leading-relaxed text-gray-600 font-medium">
                                        I agree to the <strong class="text-gray-900">Community Terms of Service</strong>. I understand that posting illegal, racist, or unauthorized content to the Discoveries Map or Wall will result in an immediate permanent profile ban, and Gateway Metal Detectors holds zero legal liability for user-generated text or media.
                                    </span>
                                </label>
                            </div>

                            <div id="signup-error" class="hidden text-red-500 text-xs font-bold bg-red-50 border border-red-200 rounded-lg px-4 py-2"></div>
                            <div id="signup-success" class="hidden text-green-600 text-xs font-bold bg-green-50 border border-green-200 rounded-lg px-4 py-2"></div>
                            <button type="submit" id="signup-submit" disabled class="w-full bg-gray-300 text-gray-500 font-black uppercase tracking-widest text-xs py-4 rounded-lg cursor-not-allowed transition-all shadow-md">Accept Terms to Sign Up</button>
                        </form>

                        <!-- OAuth Divider -->
                        <div class="flex items-center gap-4 my-6">
                            <div class="flex-1 h-px bg-gray-200"></div>
                            <span class="text-[10px] font-bold uppercase tracking-widest text-gray-400">Or continue with</span>
                            <div class="flex-1 h-px bg-gray-200"></div>
                        </div>

                        <!-- OAuth Buttons -->
                        <div class="flex gap-3">
                            <button id="oauth-google" class="flex-1 flex items-center justify-center gap-2 bg-white border border-gray-300 rounded-lg py-3 hover:bg-gray-50 hover:border-gray-400 transition-colors shadow-sm group">
                                <svg class="w-5 h-5" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 01-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
                                <span class="text-xs font-bold text-gray-700 group-hover:text-gray-900">Google</span>
                            </button>
                            <button id="oauth-microsoft" class="flex-1 flex items-center justify-center gap-2 bg-white border border-gray-300 rounded-lg py-3 hover:bg-gray-50 hover:border-gray-400 transition-colors shadow-sm group">
                                <svg class="w-5 h-5" viewBox="0 0 24 24"><rect x="1" y="1" width="10" height="10" fill="#F25022"/><rect x="13" y="1" width="10" height="10" fill="#7FBA00"/><rect x="1" y="13" width="10" height="10" fill="#00A4EF"/><rect x="13" y="13" width="10" height="10" fill="#FFB900"/></svg>
                                <span class="text-xs font-bold text-gray-700 group-hover:text-gray-900">Microsoft</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modalEl);
        bindEvents();
        return modalEl;
    }

    function bindEvents() {
        const backdrop = document.getElementById('auth-backdrop');
        const closeBtn = document.getElementById('auth-close-btn');
        const tabSignin = document.getElementById('tab-signin');
        const tabSignup = document.getElementById('tab-signup');
        const signinForm = document.getElementById('signin-form');
        const signupForm = document.getElementById('signup-form');
        const tosCheckbox = document.getElementById('tos-checkbox');
        const signupSubmit = document.getElementById('signup-submit');

        // Close handlers
        backdrop.addEventListener('click', close);
        closeBtn.addEventListener('click', close);

        // Tab switching
        tabSignin.addEventListener('click', () => switchTab('signin'));
        tabSignup.addEventListener('click', () => switchTab('signup'));

        // ToS checkbox controls submit
        tosCheckbox.addEventListener('change', () => {
            if (tosCheckbox.checked) {
                signupSubmit.disabled = false;
                signupSubmit.className = 'w-full bg-amber-600 text-white font-black uppercase tracking-widest text-xs py-4 rounded-lg hover:bg-amber-700 transition-all shadow-md cursor-pointer';
                signupSubmit.textContent = 'Create Account';
            } else {
                signupSubmit.disabled = true;
                signupSubmit.className = 'w-full bg-gray-300 text-gray-500 font-black uppercase tracking-widest text-xs py-4 rounded-lg cursor-not-allowed transition-all shadow-md';
                signupSubmit.textContent = 'Accept Terms to Sign Up';
            }
        });

        // Sign In submit
        signinForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const errorEl = document.getElementById('signin-error');
            errorEl.classList.add('hidden');
            const email = document.getElementById('signin-email').value;
            const password = document.getElementById('signin-password').value;
            const submitBtn = document.getElementById('signin-submit');
            submitBtn.textContent = 'Signing In...';
            submitBtn.disabled = true;

            try {
                const sb = window._supabase;
                if (!sb) throw new Error('Auth service not available');
                const { error } = await sb.auth.signInWithPassword({ email, password });
                if (error) throw error;
                close();
            } catch (err) {
                errorEl.textContent = err.message || 'Sign in failed. Please try again.';
                errorEl.classList.remove('hidden');
            } finally {
                submitBtn.textContent = 'Sign In';
                submitBtn.disabled = false;
            }
        });

        // Sign Up submit
        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const errorEl = document.getElementById('signup-error');
            const successEl = document.getElementById('signup-success');
            errorEl.classList.add('hidden');
            successEl.classList.add('hidden');
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const submitBtn = document.getElementById('signup-submit');
            submitBtn.textContent = 'Creating Account...';
            submitBtn.disabled = true;

            try {
                const sb = window._supabase;
                if (!sb) throw new Error('Auth service not available');
                const { error } = await sb.auth.signUp({ email, password });
                if (error) throw error;
                successEl.textContent = 'Account created! Check your email for verification, then sign in.';
                successEl.classList.remove('hidden');
                signupForm.reset();
                document.getElementById('tos-checkbox').checked = false;
                submitBtn.className = 'w-full bg-gray-300 text-gray-500 font-black uppercase tracking-widest text-xs py-4 rounded-lg cursor-not-allowed transition-all shadow-md';
                submitBtn.textContent = 'Accept Terms to Sign Up';
            } catch (err) {
                errorEl.textContent = err.message || 'Sign up failed. Please try again.';
                errorEl.classList.remove('hidden');
                submitBtn.textContent = 'Create Account';
                submitBtn.disabled = false;
            }
        });

        // OAuth
        document.getElementById('oauth-google').addEventListener('click', async () => {
            const sb = window._supabase;
            if (!sb) return;
            await sb.auth.signInWithOAuth({ provider: 'google' });
        });

        document.getElementById('oauth-microsoft').addEventListener('click', async () => {
            const sb = window._supabase;
            if (!sb) return;
            await sb.auth.signInWithOAuth({ provider: 'azure' });
        });
    }

    function switchTab(tab) {
        const tabSignin = document.getElementById('tab-signin');
        const tabSignup = document.getElementById('tab-signup');
        const signinForm = document.getElementById('signin-form');
        const signupForm = document.getElementById('signup-form');

        if (tab === 'signin') {
            tabSignin.className = 'flex-1 py-3 text-xs font-black uppercase tracking-widest text-amber-600 border-b-2 border-amber-600 transition-all';
            tabSignup.className = 'flex-1 py-3 text-xs font-black uppercase tracking-widest text-gray-400 border-b-2 border-transparent hover:text-gray-600 transition-all';
            signinForm.classList.remove('hidden');
            signupForm.classList.add('hidden');
        } else {
            tabSignup.className = 'flex-1 py-3 text-xs font-black uppercase tracking-widest text-amber-600 border-b-2 border-amber-600 transition-all';
            tabSignin.className = 'flex-1 py-3 text-xs font-black uppercase tracking-widest text-gray-400 border-b-2 border-transparent hover:text-gray-600 transition-all';
            signupForm.classList.remove('hidden');
            signinForm.classList.add('hidden');
        }
    }

    function open(tab = 'signin') {
        buildModal();
        switchTab(tab);

        // Clear previous errors/success
        document.getElementById('signin-error')?.classList.add('hidden');
        document.getElementById('signup-error')?.classList.add('hidden');
        document.getElementById('signup-success')?.classList.add('hidden');

        modalEl.classList.remove('hidden');
        document.body.style.overflow = 'hidden';

        requestAnimationFrame(() => {
            document.getElementById('auth-backdrop').style.opacity = '1';
            const card = document.getElementById('auth-card');
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
        });
    }

    function close() {
        if (!modalEl) return;
        document.getElementById('auth-backdrop').style.opacity = '0';
        const card = document.getElementById('auth-card');
        card.style.opacity = '0';
        card.style.transform = 'scale(0.95)';
        document.body.style.overflow = '';

        setTimeout(() => {
            modalEl.classList.add('hidden');
        }, 300);
    }

    // ── Expose globally ─────────────────────────────────────────
    window.GatewayAuthModal = { open, close };

})();
