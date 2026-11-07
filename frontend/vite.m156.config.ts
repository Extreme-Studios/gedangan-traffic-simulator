import{defineConfig}from'vite';import react from'@vitejs/plugin-react';export default defineConfig({plugins:[react()],publicDir:false,build:{outDir:'dist-m156',rollupOptions:{input:'m156.html'}}});
