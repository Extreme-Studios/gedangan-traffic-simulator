@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Project virtual environment missing. Read MILESTONE_03_README.md.
 exit /b 1
)
".venv\Scripts\python.exe" configuration\network-m03\build_network.py
endlocal
