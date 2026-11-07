@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python 3.12+ diperlukan. Baca MILESTONE_02_README.md.
  pause
  exit /b 1
)
python configuration\start_mapping_m02.py %*
if errorlevel 1 pause
endlocal
