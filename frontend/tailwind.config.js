/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'brand-dark': '#0d1117',
        'brand-light': '#ffffff',
        'brand-accent': '#58a6ff',
      },
    },
  },
  plugins: [],
}
