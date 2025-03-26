import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/post-audio': {
        target: process.env.VITE_BACKEND_URL, // Use the .env variable
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/post-audio/, ''),
      },
    },
  },
});
