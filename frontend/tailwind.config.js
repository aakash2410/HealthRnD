/** @type {import('tailwindcss').Config} */
export default {
    content: [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: "class",
    theme: {
        extend: {
            "colors": {
                "secondary-fixed-dim": "#b9c7e0",
                "tertiary-fixed": "#e1e0ff",
                "surface": "#f7f9fb",
                "primary-container": "#131b2e",
                "on-error": "#ffffff",
                "surface-variant": "#e0e3e5",
                "on-primary-container": "#7c839b",
                "primary-fixed-dim": "#bec6e0",
                "surface-bright": "#f7f9fb",
                "primary": "#000000",
                "inverse-surface": "#2d3133",
                "on-primary-fixed": "#131b2e",
                "on-tertiary-fixed": "#07006c",
                "on-tertiary-container": "#7073ff",
                "on-secondary-container": "#57657b",
                "on-tertiary": "#ffffff",
                "inverse-primary": "#bec6e0",
                "surface-tint": "#565e74",
                "on-secondary-fixed": "#0d1c2f",
                "surface-container-low": "#f2f4f6",
                "error": "#ba1a1a",
                "on-tertiary-fixed-variant": "#2f2ebe",
                "on-background": "#191c1e",
                "secondary": "#515f74",
                "on-primary": "#ffffff",
                "primary-fixed": "#dae2fd",
                "on-surface-variant": "#45464d",
                "on-error-container": "#93000a",
                "surface-dim": "#d8dadc",
                "outline": "#76777d",
                "inverse-on-surface": "#eff1f3",
                "secondary-fixed": "#d5e3fd",
                "error-container": "#ffdad6",
                "surface-container-lowest": "#ffffff",
                "tertiary": "#000000",
                "tertiary-fixed-dim": "#c0c1ff",
                "secondary-container": "#d5e3fd",
                "surface-container": "#eceef0",
                "on-secondary": "#ffffff",
                "surface-container-highest": "#e0e3e5",
                "on-surface": "#191c1e",
                "outline-variant": "#c6c6cd",
                "on-primary-fixed-variant": "#3f465c",
                "surface-container-high": "#e6e8ea",
                "tertiary-container": "#07006c",
                "on-secondary-fixed-variant": "#3a485c",
                "background": "#f7f9fb"
            },
            "borderRadius": {
                "DEFAULT": "0.125rem",
                "lg": "0.25rem",
                "xl": "0.5rem",
                "full": "0.75rem"
            },
            "spacing": {
                "margin-mobile": "16px",
                "margin-desktop": "32px",
                "unit": "4px",
                "gutter": "16px",
                "max-width": "1440px"
            },
            "fontFamily": {
                "headline-md": ["Inter"],
                "data-mono": ["JetBrains Mono"],
                "label-md": ["Inter"],
                "display-lg": ["Inter"],
                "title-lg": ["Inter"],
                "headline-lg": ["Inter"],
                "body-lg": ["Inter"],
                "body-md": ["Inter"]
            },
            "fontSize": {
                "headline-md": ["24px", { "lineHeight": "32px", "fontWeight": "600" }],
                "data-mono": ["13px", { "lineHeight": "18px", "fontWeight": "500" }],
                "label-md": ["12px", { "lineHeight": "16px", "letterSpacing": "0.05em", "fontWeight": "600" }],
                "display-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                "title-lg": ["20px", { "lineHeight": "28px", "fontWeight": "600" }],
                "headline-lg": ["32px", { "lineHeight": "40px", "letterSpacing": "-0.01em", "fontWeight": "600" }],
                "body-lg": ["16px", { "lineHeight": "24px", "fontWeight": "400" }],
                "body-md": ["14px", { "lineHeight": "20px", "fontWeight": "400" }]
            }
        }
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/container-queries')
    ],
}
