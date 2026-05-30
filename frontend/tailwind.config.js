/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#FF6B6B",
          secondary: "#4ECDC4",
          accent: "#FFE66D",
          dark: "#2C3E50",
          light: "#F7F9FC",
        },
        glucose: {
          baseline: "#4ECDC4",
          elevated: "#FFB84D",
          high: "#FF6B6B",
          low: "#95E1D3",
        },
        energy: {
          storage: "#FFB84D",
          action: "#4ECDC4",
          risk: "#FF6B6B",
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

