@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" -m backend.gedangan.m09_checkpoint --verify
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m backend.gedangan.m09_export
if errorlevel 1 goto fail
pushd frontend
call npx --no-install tsc --noEmit
if errorlevel 1 goto frontend_fail
call npx --no-install vite build --config vite.presentation.config.ts
if errorlevel 1 goto frontend_fail
popd
".venv\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 goto fail
node tests\m09\test_core.cjs
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m backend.gedangan.m09_checkpoint --verify
if errorlevel 1 goto fail
echo Build dan pemeriksaan otomatis selesai. Visual acceptance membutuhkan browser QA aktual.
exit /b 0
:frontend_fail
popd
:fail
echo Rebuild gagal. Bukti lama tidak ditimpa; periksa pesan di atas.
pause
exit /b 1
