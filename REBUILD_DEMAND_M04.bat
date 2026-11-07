@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" configuration\demand-m04\build_demand.py
endlocal
