/**
 * @fileoverview Gateway Metal Detectors — Self-Healing Layer
 * Error boundaries, fallback states, and graceful degradation.
 * @namespace GatewayHeal
 */

'use strict';

const GatewayHeal = {

  /**
   * Handle inventory load failure with an in-page fallback state.
   * @param {Error} error - The error that occurred
   */
  handleInventoryError(error) {
    console.warn('[GatewayHeal] Inventory load failed — activating fallback:', error.message);

    const grid = document.getElementById('products-grid');
    if (!grid) return;

    grid.innerHTML = `
      <div class="error-state glass-card" role="alert" aria-live="assertive">
        <div class="error-icon" aria-hidden="true">📡</div>
        <h3>Signal Lost</h3>
        <p>We couldn't load our current inventory. Please visit us in person or refresh the page.</p>
        <address>
          <strong>Hagler's Flea Market</strong><br>
          1549 Barton St E, Hamilton, ON<br>
          Walk-ins Welcome — Ask for Rick
        </address>
        <button class="btn btn--secondary" onclick="location.reload()">↺ Retry Signal</button>
      </div>`;

    const syncEl = document.getElementById('sync-status');
    if (syncEl) {
      syncEl.classList.add('sync-badge--error');
      const textEl = syncEl.querySelector('.sync-text');
      if (textEl) textEl.textContent = 'Sync unavailable — visit us in person';
    }
  },

  /**
   * Attach onerror fallbacks to all images.
   */
  initImageFallbacks() {
    document.querySelectorAll('img').forEach(img => {
      img.addEventListener('error', function () {
        this.removeAttribute('src');
        this.setAttribute('aria-label', 'Image unavailable');
      });
    });
  },

  /**
   * Global error sentinel — logs uncaught errors to console.
   */
  initSentinel() {
    window.addEventListener('error', e => {
      console.error('[GatewayHeal] Uncaught error:', e?.error?.message ?? e.message);
    });
    window.addEventListener('unhandledrejection', e => {
      console.error('[GatewayHeal] Unhandled promise rejection:', e.reason);
    });
  },

  /** Initialize all self-healing systems. */
  init() {
    this.initSentinel();
    this.initImageFallbacks();
    console.log('[GatewayHeal] 🛡️ Self-healing layer active');
  }
};

GatewayHeal.init();
