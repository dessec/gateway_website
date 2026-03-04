import React from 'react';

/**
 * Hero component displaying the main landing section.
 * Features animated visuals, key value propositions, and primary calls to action.
 *
 * @returns {React.ReactElement} The stateless Hero component.
 */
const Hero = () => {
    return (
        <section id="hero" className="hero" aria-label="Gateway Metal Detectors — Hero">
            {/* Animated scan line */}
            <div className="scan-line" aria-hidden="true"></div>

            {/* Background signal arcs */}
            <div className="hero-arcs" aria-hidden="true">
                <div className="arc arc--1"></div>
                <div className="arc arc--2"></div>
                <div className="arc arc--3"></div>
                <div className="arc arc--4"></div>
            </div>

            <div className="container hero__content">
                {/* Hero Background Image */}
                <div className="hero__image-wrapper" aria-hidden="true" style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    zIndex: -1,
                    opacity: 0.3, /* Matches brand guidelines for dark overlay */
                    overflow: 'hidden'
                }}>
                    <img
                        src="/website/screenshots/home.jpg"
                        alt="Gateway Metal Detectors Hero Background"
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                        onError={(e) => {
                            e.currentTarget.removeAttribute('src');
                            e.currentTarget.setAttribute('aria-label', 'Image unavailable');
                            e.currentTarget.style.display = 'none';
                        }}
                    />
                </div>

                {/* Eyebrow tag */}
                <div className="hero__eyebrow" aria-label="Hamilton's metal detecting experts">
                    <span className="eyebrow-dot" aria-hidden="true"></span>
                    Hamilton, Ontario — Official Nokta Authorized Dealer
                </div>

                {/* Main headline */}
                <h1 className="hero__headline">
                    Every Signal<br />
                    <em>Tells a Story</em>
                </h1>

                {/* Sub-copy */}
                <p className="hero__body">
                    Southern Ontario's fields, Lake Erie beaches, and abandoned farmsteads
                    are full of history waiting to be found. Gateway Metal Detectors is Hamilton's
                    local expert — here to help you uncover it.
                </p>

                {/* CTAs */}
                <div className="hero__ctas">
                    <a href="#products" className="btn btn--primary btn--xl btn--pulse" id="hero-cta-primary">
                        Start Your Hunt
                    </a>
                    <a href="#about" className="btn btn--ghost btn--xl" id="hero-cta-secondary">
                        Meet Rick →
                    </a>
                </div>

                {/* Stats row */}
                <div className="hero__stats" aria-label="Key stats">
                    <div className="hero__stat">
                        <span className="stat-value mono">6</span>
                        <span className="stat-label">Nokta Models</span>
                    </div>
                    <div className="stat-sep" aria-hidden="true"></div>
                    <div className="hero__stat">
                        <span className="stat-value mono">✓</span>
                        <span className="stat-label">Official Dealer</span>
                    </div>
                    <div className="stat-sep" aria-hidden="true"></div>
                    <div className="hero__stat">
                        <span className="stat-value mono">∞</span>
                        <span className="stat-label">Finds Waiting</span>
                    </div>
                </div>
            </div>

            {/* Scroll indicator */}
            <div className="hero__scroll" aria-hidden="true">
                <div className="scroll-line"></div>
                <span>Scroll</span>
            </div>
        </section>
    );
};

export default Hero;
