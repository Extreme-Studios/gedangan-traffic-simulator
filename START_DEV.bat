@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python 3.12+ belum tersedia pada PATH. Baca README.md.
  pause
  exit /b 1
)
python configuration\start_dev.py %*
if errorlevel 1 pause
endlocal
