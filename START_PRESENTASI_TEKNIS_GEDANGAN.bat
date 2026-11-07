@echo off
setlocal
cd /d "%~dp0"
set "M11_PY=pythonw.exe"
if exist ".venv\Scripts\pythonw.exe" set "M11_PY=.venv\Scripts\pythonw.exe"
if /I "%~1"=="--no-open" (
 if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" -m backend.gedangan.m11_launch --no-open
 ) else (
  python -m backend.gedangan.m11_launch --no-open
 )
 exit /b
)
start "" /b "%M11_PY%" -m backend.gedangan.m11_launch
