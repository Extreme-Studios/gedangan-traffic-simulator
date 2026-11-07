import {defineConfig} from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({plugins:[react()],build:{outDir:'dist-m02',rollupOptions:{input:'mapping.html'},target:'es2022'},server:{host:'127.0.0.1',port:5174,strictPort:true},preview:{host:'127.0.0.1',port:5174,strictPort:true}});
