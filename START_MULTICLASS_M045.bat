@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" configuration\access-m045\start_preview.py %*
endlocal
