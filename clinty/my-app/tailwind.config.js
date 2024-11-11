/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],

  theme: {
    extend: {
      colors: {
        'bluely': '#4d88f3',
        'greyiaa': "#f4f4f7",
      },
    }
  },

  plugins: [
    require('daisyui'),
  ]
};
