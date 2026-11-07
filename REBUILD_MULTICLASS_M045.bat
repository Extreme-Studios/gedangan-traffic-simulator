@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" configuration\access-m045\rebuild.py
endlocal
