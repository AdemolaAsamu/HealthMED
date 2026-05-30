/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "Segoe UI", "Roboto", "Helvetica Neue", "Arial", "sans-serif"],
        display: ["Manrope", "Inter", "Segoe UI", "Roboto", "Helvetica Neue", "Arial", "sans-serif"],
      },
      colors: {
        brand: {
          primary: "#C83E3E",
          secondary: "#167C77",
          accent: "#F4D35E",
          dark: "#243447",
          light: "#F6F8FA",
        },
        glucose: {
          baseline: "#167C77",
          elevated: "#B7791F",
          high: "#C53030",
          low: "#D6F5EF",
        },
        energy: {
          storage: "#B7791F",
          action: "#167C77",
          risk: "#C53030",
        }
      },
      animation: {
        "float": "float 3s ease-in-out infinite",
        "pulse-glow": "pulse-glow 2s ease-in-out infinite",
        "glucose-rise": "glucose-rise 2s ease-out forwards",
        "glucose-fall": "glucose-fall 3s ease-in forwards",
        "blood-flow": "blood-flow 4s linear infinite",
      },
      keyframes: {
        float: {
          "0%, 100%": { transform: "translateY(0px)" },
          "50%": { transform: "translateY(-20px)" },
        },
        "pulse-glow": {
          "0%, 100%": { opacity: "1", transform: "scale(1)" },
          "50%": { opacity: "0.7", transform: "scale(1.05)" },
        },
        "glucose-rise": {
          "0%": { transform: "translateY(200px)", opacity: "0" },
          "100%": { transform: "translateY(0px)", opacity: "1" },
        },
        "glucose-fall": {
          "0%": { transform: "translateY(0px)", opacity: "1" },
          "100%": { transform: "translateY(200px)", opacity: "0" },
        },
        "blood-flow": {
          "0%": { transform: "translateX(-100%)" },
          "100%": { transform: "translateX(100%)" },
        },
      },
    },
  },
  plugins: [],
}

