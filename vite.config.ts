import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Explicitly listen on all interfaces
    allowedHosts: true, 
  },
  preview: {
    host: '0.0.0.0',
    allowedHosts: true,
    port: 4173
  }
});