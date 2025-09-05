import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Default backend: localhost (dev). Override in production via VITE_BACKEND_URL
const backendUrl = process.env.VITE_BACKEND_URL || "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  define: {
    __BACKEND_URL__: JSON.stringify(backendUrl),
  },
});
