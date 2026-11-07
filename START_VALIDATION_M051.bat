@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" configuration\validation-m051\start_preview.py %*
