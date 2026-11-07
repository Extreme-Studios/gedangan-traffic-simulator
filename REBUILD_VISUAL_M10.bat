@echo off
setlocal
cd /d "%~dp0frontend"
node node_modules\typescript\bin\tsc --noEmit
if errorlevel 1 exit /b 1
node node_modules\vite\bin\vite.js build --config vite.visual.config.ts
if errorlevel 1 exit /b 1
cd ..
node tests\m10\test_core.cjs
