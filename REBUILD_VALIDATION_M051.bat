@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" -c "from backend.gedangan.m051_verify import assert_baseline; assert_baseline()"
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m051_geometry
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m051_controls
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m051_causality
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m051_additional
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m051_verify
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m051_publish
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m unittest discover -s tests -v > documentation\m051\final-regression.txt 2>&1
if errorlevel 1 exit /b 1
cd frontend
call npx tsc --noEmit > ..\documentation\m051\typescript.txt 2>&1
if errorlevel 1 exit /b 1
call npx vite build --config vite.validation.config.ts > ..\documentation\m051\vite-build.txt 2>&1
if errorlevel 1 exit /b 1
cd ..
".venv\Scripts\python.exe" -m backend.gedangan.m051_report
endlocal
