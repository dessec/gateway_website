/**
 * @fileoverview Gateway Metal Detectors — Main Script
 * Loads inventory.json, renders product cards, handles scroll reveal and nav behavior.
 */

'use strict';

/** @type {Object|null} Loaded inventory data */
let inventory = null;

/**
 * Fetch and return inventory data from inventory.json.
 * @returns {Promise<Object>}
 */
async function loadInventory() {
  const res = await fetch('inventory.json');
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

/**
 * Build a stock badge DOM element.
 * @param {boolean} inStock
 * @returns {HTMLElement}
 */
function buildStockBadge(inStock) {
  const badge = document.createElement('span');
  badge.className = `stock-badge stock-badge--${inStock ? 'in' : 'out'}`;
  badge.setAttribute('role', 'status');
  badge.setAttribute('aria-label', inStock ? 'In Stock' : 'Out of Stock');

  const dot = document.createElement('span');
  dot.className = 'stock-dot';
  dot.setAttribute('aria-hidden', 'true');

  const label = document.createElement('span');
  label.textContent = inStock ? 'In Stock' : 'Out of Stock';

  badge.appendChild(dot);
  badge.appendChild(label);
  return badge;
}

/**
 * Generate an inline SVG detector graphic.
 * @param {boolean} inStock - Drives the indicator dot color.
 * @returns {string} SVG markup string
 */
function detectorSVG(inStock) {
  const signalColor = inStock ? '#22C55E' : '#6B7280';
  const signalGlow = inStock ? 'rgba(34,197,94,0.35)' : 'rgba(107,114,128,0.2)';
  return `<svg viewBox="0 0 80 130" fill="none" xmlns="http://www.w3.org/2000/svg" class="detector-gfx" aria-hidden="true">
    <!-- Shaft -->
    <rect x="37" y="4" width="6" height="68" rx="3" fill="rgba(200,151,42,0.55)"/>
    <!-- Handle grip -->
    <rect x="30" y="60" width="20" height="14" rx="5" fill="rgba(200,151,42,0.35)"/>
    <!-- Lower rod -->
    <rect x="39" y="74" width="2" height="28" rx="1" fill="rgba(200,151,42,0.4)"/>
    <!-- Search coil -->
    <ellipse cx="40" cy="115" rx="26" ry="8" stroke="rgba(200,151,42,0.55)" stroke-width="1.5" fill="none"/>
    <ellipse cx="40" cy="115" rx="14" ry="4" stroke="rgba(200,151,42,0.3)" stroke-width="1" fill="none"/>
    <!-- Signal indicator -->
    <circle cx="40" cy="24" r="5" fill="${signalColor}"/>
    <circle cx="40" cy="24" r="10" stroke="${signalGlow}" stroke-width="1.5" fill="none"/>
    <circle cx="40" cy="24" r="15" stroke="${signalGlow.replace('0.35', '0.12').replace('0.2', '0.08')}" stroke-width="1" fill="none"/>
  </svg>`;
}

/**
 * Render a single product card article element.
 * @param {Object} product
 * @param {number} index - Used to stagger animation delay
 * @returns {HTMLElement}
 */
function renderProductCard(product, index) {
  const card = document.createElement('article');
  card.className = 'product-card glass-card';
  card.setAttribute('role', 'listitem');
  card.id = `product-${product.id}`;

  const badge = buildStockBadge(product.inStock);

  card.innerHTML = `
    <div class="product-card__visual">
      <div class="product-visual-pattern"></div>
      ${product.isNew ? '<div class="new-tag">NEW</div>' : ''}
      ${detectorSVG(product.inStock)}
      <div class="product-arcs" aria-hidden="true">
        <div class="p-arc p-arc--1"></div>
        <div class="p-arc p-arc--2"></div>
        <div class="p-arc p-arc--3"></div>
      </div>
    </div>

    <div class="product-card__body">
      <div class="product-card__header">
        <span class="product-brand mono">${product.brand}</span>
        <span class="product-badge-slot"></span>
      </div>
      <h3 class="product-name">${product.name}</h3>
      <p class="product-tagline">${product.tagline}</p>

      <div class="product-specs">
        <div class="spec-row">
          <span class="spec-label">Frequency</span>
          <span class="spec-value">${product.frequencies}</span>
        </div>
        <div class="spec-row">
          <span class="spec-label">Waterproof</span>
          <span class="spec-value">${product.waterproof ? '✓ Yes' : '✗ No'}</span>
        </div>
        <div class="spec-row">
          <span class="spec-label">Best For</span>
          <span class="spec-value">${product.bestFor}</span>
        </div>
      </div>

      <div class="product-card__footer">
        <div class="product-price">${product.price}</div>
        <button
          class="btn btn--secondary btn--sm"
          id="cta-${product.id}"
          aria-label="Contact to Order ${product.name}"
          data-product-id="${product.id}">
          Contact to Order
        </button>
      </div>
    </div>`;

  // Inject badge into its slot (DOM element, not innerHTML)
  card.querySelector('.product-badge-slot').replaceWith(badge);

  // Staggered entrance
  card.style.transitionDelay = `${index * 70}ms`;
  requestAnimationFrame(() => requestAnimationFrame(() => card.classList.add('loaded')));

  // CTA click → scroll to contact
  card.querySelector(`#cta-${product.id}`)?.addEventListener('click', () => {
    handleProductCTA(product);
  });

  return card;
}

/**
 * Render skeleton placeholder cards while inventory loads.
 * @param {number} count
 */
function renderSkeletons(count = 6) {
  const grid = document.getElementById('products-grid');
  if (!grid) return;

  for (let i = 0; i < count; i++) {
    const s = document.createElement('div');
    s.className = 'product-card product-card--skeleton glass-card';
    s.setAttribute('aria-hidden', 'true');
    s.innerHTML = `
      <div class="skeleton-visual"></div>
      <div class="product-card__body">
        <div class="skeleton-line skeleton-line--short"></div>
        <div class="skeleton-line skeleton-line--long"></div>
        <div class="skeleton-line skeleton-line--medium"></div>
      </div>`;
    grid.appendChild(s);
  }
}

/**
 * Render all product cards from loaded inventory.
 * @param {Object} inv - Inventory data
 */
function renderProducts(inv) {
  const grid = document.getElementById('products-grid');
  if (!grid) return;

  grid.innerHTML = '';
  inv.products.forEach((p, i) => grid.appendChild(renderProductCard(p, i)));
  updateSyncBadge(inv.lastSynced);
}

/**
 * Update the sync status badge with the last-synced timestamp.
 * @param {string} isoTimestamp
 */
function updateSyncBadge(isoTimestamp) {
  const el = document.getElementById('sync-status');
  if (!el) return;

  const date = new Date(isoTimestamp);
  const formatted = date.toLocaleDateString('en-CA', { month: 'short', day: 'numeric', year: 'numeric' });
  const textEl = el.querySelector('.sync-text');
  if (textEl) textEl.textContent = `Live stock via radioworld.ca — synced ${formatted}`;
  el.classList.add('sync-badge--active');
}

/**
 * Handle product CTA button click to open the contact modal.
 * @param {Object} product
 */
function handleProductCTA(product) {
  const modal = document.getElementById('contact-modal');
  if (modal) {
    modal.showModal();
    modal.classList.add('open');
  }
}

/**
 * Initialize modal close functionality.
 */
function initModal() {
  const modal = document.getElementById('contact-modal');
  const closeBtn = modal?.querySelector('.modal__close');

  closeBtn?.addEventListener('click', () => {
    modal.close();
    modal.classList.remove('open');
  });

  // Close when clicking outside of the modal window (on backdrop)
  modal?.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.close();
      modal.classList.remove('open');
    }
  });
}

/**
 * Sticky nav — adds .nav--scrolled class once hero is out of view.
 */
function initNav() {
  const nav = document.getElementById('main-nav');
  const hero = document.getElementById('hero');
  if (!nav || !hero) return;

  const obs = new IntersectionObserver(
    ([entry]) => nav.classList.toggle('nav--scrolled', !entry.isIntersecting),
    { threshold: 0 }
  );
  obs.observe(hero);

  // Mobile menu toggle
  const toggle = document.querySelector('.nav__mobile-toggle');
  const links = document.querySelector('.nav__links');

  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    links?.classList.toggle('open', !open);
  });

  // Close mobile menu on link click
  links?.querySelectorAll('a').forEach(a => {
    a.addEventListener('click', () => {
      links.classList.remove('open');
      toggle?.setAttribute('aria-expanded', 'false');
    });
  });
}

/**
 * IntersectionObserver-based scroll reveal.
 * Any element with class .reveal is animated when it enters the viewport.
 */
function initScrollReveal() {
  const els = document.querySelectorAll('.reveal');
  if (!els.length) return;

  const obs = new IntersectionObserver(
    entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          obs.unobserve(e.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  els.forEach(el => obs.observe(el));
}

/**
 * Main boot sequence.
 */
async function init() {
  console.log('[Gateway] 🎯 v1.0.0 — Initializing');

  initNav();
  initScrollReveal();
  initModal();
  renderSkeletons(6);

  try {
    inventory = await loadInventory();
    renderProducts(inventory);
    console.log(`[Gateway] ✅ Loaded ${inventory.products.length} products from ${inventory.syncSource}`);
  } catch (err) {
    console.error('[Gateway] ❌ Inventory load failed:', err);
    GatewayHeal.handleInventoryError(err);
  }
}

document.addEventListener('DOMContentLoaded', init);
