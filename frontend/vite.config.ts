/// <reference types="vitest/config" />
import { defineConfig } from 'vitest/config'
import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: path.resolve(__dirname, "./src/setupTests.ts"),
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173, // Puerto del servidor de desarrollo (opcional, 5173 es el predeterminado)
    host: '0.0.0.0', // Host del servidor de desarrollo (opcional, 'localhost' es el predeterminado)
    proxy: {
      '/api': {
        target: 'http://192.168.0.159:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''), // replaces /api with ''
      },
    },
  },
})
