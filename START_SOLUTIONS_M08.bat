@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" configuration\scenarios-m08\start_preview.py %*
