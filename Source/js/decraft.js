'use strict';

/**
 * decraft.js - Gateway Adaptation
 * Handles simple UI interactions like the Accordion logic and Contact Modal targeting the specific layout.
 */

function initAccordions() {
    const accButtons = document.querySelectorAll('.acc-btn');

    accButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            // Toggle active state
            const item = this.parentElement;

            // Close others (optional based on behavior, often nice)
            document.querySelectorAll('.acc-item').forEach(otherItem => {
                if (otherItem !== item) {
                    otherItem.classList.remove('active');
                }
            });

            item.classList.toggle('active');

            // Update the span indicator
            const span = this.querySelector('span');
            if (item.classList.contains('active')) {
                span.textContent = '−';
            } else {
                span.textContent = '+';
            }
        });
    });
}

function initContactModal() {
    const modal = document.getElementById('contact-modal');
    const openBtns = document.querySelectorAll('.btn--contact-modal');
    const closeBtn = modal?.querySelector('.modal__close');

    openBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            if (modal) {
                modal.showModal();
                modal.classList.add('open');
            }
        });
    });

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

document.addEventListener('DOMContentLoaded', () => {
    initAccordions();
    initContactModal();
});
