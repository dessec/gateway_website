/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./*.html", "./*.js"],
    theme: {
        extend: {
            colors: {
                void: "#0A0E1A",
                gold: "#C8972A",
                signal: "#22C55E",
            },
            fontFamily: {
                display: ["Barlow Condensed", "sans-serif"],
                body: ["Inter", "sans-serif"],
            },
            backdropBlur: {
                xs: '2px',
            },
        },
    },
    plugins: [],
}
