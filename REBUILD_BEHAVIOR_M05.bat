@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" -m backend.gedangan.m05_behavior all
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m05_sublane
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m05_spillback_fixture
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m05_provenance
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m05_analysis
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m05_safety
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m05_export
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 exit /b 1
cd frontend
call npx tsc --noEmit
if errorlevel 1 exit /b 1
call npx vite build --config vite.behavior.config.ts
if errorlevel 1 exit /b 1
cd ..
".venv\Scripts\python.exe" -m backend.gedangan.m05_report
endlocal
