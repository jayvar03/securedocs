/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#F5F2EB',
        panel: '#FCFBF7',
        ink: '#1C1B18',
        muted: '#6A665C',
        rule: '#D8D2C4',
        accent: { DEFAULT: '#1F5C5A', dark: '#174745', soft: '#DCE8E4' },
        danger: { DEFAULT: '#A33A2B', soft: '#F3DDD7' },
        role: { admin: '#1F5C5A', manager: '#A8741A', employee: '#5B6B7A' },
      },
      fontFamily: {
        serif: ['Newsreader', 'Georgia', 'serif'],
        sans: ['"IBM Plex Sans"', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'monospace'],
      },
      borderRadius: { DEFAULT: '4px' },
    },
  },
  plugins: [],
}
