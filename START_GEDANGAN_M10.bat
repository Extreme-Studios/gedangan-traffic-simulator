@echo off
setlocal
cd /d "%~dp0"
if not exist "frontend\dist-m10\visual.html" (
 echo Build M10 belum tersedia. Jalankan REBUILD_VISUAL_M10.bat.
 exit /b 1
)
set "M10_BROWSER_FLAG=--open"
if /I "%~1"=="--no-open" set "M10_BROWSER_FLAG="
if exist ".venv\Scripts\python.exe" (
 ".venv\Scripts\python.exe" -m backend.gedangan.m10_server %M10_BROWSER_FLAG%
) else (
 python -m backend.gedangan.m10_server %M10_BROWSER_FLAG%
)
if errorlevel 1 pause
