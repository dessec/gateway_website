import React from 'react';

/**
 * Header component that displays the main navigation bar.
 * Includes the brand logo, navigation links, and a call-to-action button.
 * Incorporates self-healing try/catch logic to render a fallback state upon failure.
 *
 * @returns {React.ReactElement} The stateless Header component, or a fallback UI on error.
 */
const Header = () => {
    try {
        return (
            <nav id="main-nav" className="nav" role="navigation" aria-label="Main navigation">
                <div className="container nav__inner">
                    <a href="#hero" className="nav__logo" aria-label="Gateway Metal Detectors — Home">
                        <div className="logo-mark" aria-hidden="true">🎯</div>
                        <div className="logo-text">
                            <span className="logo-wordmark">GATEWAY</span>
                            <span className="logo-sub">Metal Detectors</span>
                        </div>
                    </a>

                    <ul className="nav__links" id="nav-links" role="list">
                        <li><a href="#products">Detectors</a></li>
                        <li><a href="#about">About</a></li>
                        <li><a href="#site-footer">Visit Us</a></li>
                    </ul>

                    <a href="#products" className="btn btn--primary btn--sm nav__cta" id="nav-cta">
                        See What's In Stock
                    </a>

                    <button
                        className="nav__mobile-toggle"
                        aria-label="Toggle navigation menu"
                        aria-expanded="false"
                        aria-controls="nav-links"
                    >
                        <span aria-hidden="true"></span>
                    </button>
                </div>
            </nav>
        );
    } catch (error) {
        console.error('[GatewayHeal] Header component failed to load:', error);
        // Graceful fallback state as per self-healing mandate
        return (
            <nav id="main-nav-fallback" className="nav nav--fallback glass-card" role="navigation" aria-label="Main navigation fallback">
                <div className="container nav__inner" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div className="nav__logo">
                        <div className="logo-text">
                            <span className="logo-wordmark">GATEWAY</span>
                        </div>
                    </div>
                    <div className="error-state-inline" role="alert" style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                        <span style={{ color: 'var(--color-warning)' }}>Navigation unavailable.</span>
                        <button className="btn btn--secondary btn--sm" onClick={() => window.location.reload()}>
                            ↺ Retry
                        </button>
                    </div>
                </div>
            </nav>
        );
    }
};

export default Header;
