@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" -m backend.gedangan.m085_baseline --verify
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 goto fail
node tests\m085\test_sha256.cjs
if errorlevel 1 goto fail
pushd frontend
call npx --no-install tsc --noEmit
if errorlevel 1 goto frontend_fail
call npx --no-install vite build --config vite.survey.config.ts
if errorlevel 1 goto frontend_fail
popd
".venv\Scripts\python.exe" -m backend.gedangan.m085_baseline --verify
if errorlevel 1 goto fail
echo M08.5 rebuild selesai. QA browser aktual tetap diperlukan sebelum technical readiness PASS.
exit /b 0
:frontend_fail
popd
:fail
echo Rebuild M08.5 gagal. Baca error di atas; tidak ada generator M01-M08 yang dijalankan.
pause
exit /b 1
