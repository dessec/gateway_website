import React from 'react';

/**
 * Footer component to display navigation, contact details, and legal information.
 *
 * @returns {React.ReactElement} The stateless Footer component.
 */
const Footer = () => {
    return (
        <footer id="site-footer" className="footer" role="contentinfo">
            <div className="container">
                <div className="footer__grid">
                    {/* Brand column */}
                    <div className="footer-col">
                        <div className="footer-logo">
                            <span className="logo-wordmark">GATEWAY</span><br />
                            <span className="logo-sub">Metal Detectors</span>
                        </div>
                        <p className="footer-tagline">Every Signal Tells a Story.</p>
                        <div className="footer-nokta" id="footer-nokta-badge" aria-label="Nokta Authorized Dealer">
                            <span aria-hidden="true">✓</span> Official Nokta Authorized Dealer
                        </div>
                    </div>

                    {/* Explore column */}
                    <div className="footer-col">
                        <h4>Explore</h4>
                        <ul role="list">
                            <li><a href="#products">Metal Detectors</a></li>
                            <li><a href="#about">About Rick</a></li>
                            <li><a href="#site-footer">Visit Us</a></li>
                        </ul>
                    </div>

                    {/* Contact / Visit column */}
                    <div className="footer-col">
                        <h4>Visit & Contact Us</h4>
                        <address>
                            <p>Hagglers Flea Market</p>
                            <p>1565 Barton St. E, L8H2Y3</p>
                            <p>Hamilton, Ontario</p>
                        </address>
                        <p className="footer-note">
                            Call Ham: (905) 870-8689<br />
                            St. Catharines: (905) 931-8866<br />
                            Email: gatewaydetecting@hotmail.com<br />
                            Open Sunday 10am to 5pm. Call 7 days a week to order.
                        </p>
                    </div>
                </div>

                {/* Footer bottom bar */}
                <div className="footer__bottom">
                    <p className="footer__legal">
                        © 2026 Gateway Metal Detectors. Hamilton, Ontario. All rights reserved.
                    </p>
                    <p className="footer__sync mono">
                        inventory synced via radioworld.ca
                    </p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
