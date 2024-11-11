/** @type {import('tailwindcss').Config} */

const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  content: [
    './autohorario/templates/**/*.html',
    // Add paths to other apps if necessary
  ],
  theme: {
    extend: {
      colors: {
        'background': '#FDFBF2',
        'border': '#9A8318',
        'primary': {
          '50': '#fefde8',
          '100': '#fffec2',
          '200': '#fff988',
          '300': '#ffee45',
          '400': '#fddc08',
          '500': '#edc405',
          '600': '#cd9901',
          '700': '#a36c05',
          '800': '#87550c',
          '900': '#724511',
          '950': '#432405',
        },
        'secondary': {
          '50': '#f2fbf5',
          '100': '#e0f8e8',
          '200': '#c2f0d3',
          '300': '#93e2b0',
          '400': '#44c575',
          '500': '#35b265',
          '600': '#279250',
          '700': '#227341',
          '800': '#1f5c37',
          '900': '#1c4b30',
          '950': '#0a2917',
        },
        'tertiary': {
          '50': '#f2f9fd',
          '100': '#e4f0fa',
          '200': '#c3e2f4',
          '300': '#8dcbec',
          '400': '#39a5db',
          '500': '#2a96cd',
          '600': '#1b78ae',
          '700': '#17608d',
          '800': '#175275',
          '900': '#194561',
          '950': '#102c41',
        },
      },
      fontFamily: {
        'handwrite': ['"Patrick Hand"', ...defaultTheme.fontFamily.sans]
      }
    },
  },
  plugins: [],
};
