import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Listen on all addresses (0.0.0.0)
    allowedHosts: true, // Allow any host to access the server (fixes Render blocked host error)
  },
  preview: {
    host: true, // Listen on all addresses for preview mode
    allowedHosts: true, // Allow any host for preview mode
    port: 4173
  }
});