import typography from '@tailwindcss/typography'
import forms from '@tailwindcss/forms'
import aspectRatio from '@tailwindcss/aspect-ratio'

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#243880',
        secondary: '#1f4e75',
        tertiary: '#0071b3',
        accent: '#21a172',
        accentshadow: '#219c6fb3',
        accentlight: '#5ae0af',
        ownred: '#892323',
        ownorange: '#c37c12',
      },
      screens: {
        'custom-lg': '1400px', // Custom screen size
      },
    },
  },
  plugins: [typography, forms, aspectRatio],
}
