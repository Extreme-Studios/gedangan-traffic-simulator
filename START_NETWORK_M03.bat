@echo off
setlocal
cd /d "%~dp0"
python configuration\network-m03\start_preview.py %*
if errorlevel 1 pause
endlocal
