/** @type {import('tailwindcss').Config} */
export default {
  content: [
      "./index.html",
      "./src/**/*.{js,ts,jsx,tsx}",
      'node_modules/flowbite-react/**/*.{js,jsx,ts,tsx}'
  ],
  theme: {
      extend: {
          width: {
              '64': '16rem', // Add an explicit width definition for w-64
          },
      },
  },
  plugins: [
      require('flowbite/plugin')
  ],
}