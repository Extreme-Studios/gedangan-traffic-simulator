@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" configuration\demand-m04\start_preview.py %*
endlocal
