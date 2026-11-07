@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" configuration\behavior-m05\start_preview.py %*
endlocal
