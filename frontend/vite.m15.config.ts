import{defineConfig}from'vite';import react from'@vitejs/plugin-react';export default defineConfig({plugins:[react()],publicDir:false,build:{outDir:'dist-m15',rollupOptions:{input:'m15.html'}}});
