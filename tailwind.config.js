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
        'primary': '#FDDC08',
        'secondary': '#44C575',
        'tertiary': '#39A5DB',
      },
      fontFamily: {
        'handwrite': ['"Patrick Hand"', ...defaultTheme.fontFamily.sans]
      }
    },
  },
  plugins: [],
};
