/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'brand-dark': '#000000', // Pure Black
        'brand-light': '#ffffff', // Pure White
        'brand-gray': '#f5f5f7',  // Modern Light Gray
        'brand-accent': '#58a6ff',
      },
    },
  },
  plugins: [],
}
