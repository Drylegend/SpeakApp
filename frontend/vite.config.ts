import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/post-audio': {
        target: 'speakapp-production-1a3a.up.railway.app',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/post-audio/, ''),
      },
    },
  },
});
