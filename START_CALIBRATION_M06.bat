@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" configuration\calibration-m06\start_preview.py %*
