@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Python lokal proyek belum tersedia. Jalankan setup proyek yang sudah ada.
 pause
 exit /b 1
)
if not exist "frontend\dist-m085\survey.html" (
 echo Build M08.5 belum tersedia. Jalankan REBUILD_SURVEY_M085.bat dahulu.
 pause
 exit /b 1
)
echo GEDANGAN FIELD SURVEY WORKBENCH M08.5
echo Buka http://127.0.0.1:5184/survey.html
echo Server lokal: UI 5184 / API 8774. Tidak memerlukan Node atau internet setelah build.
echo Data lapangan tidak dibuat otomatis. M09 tidak dimulai.
".venv\Scripts\python.exe" -m backend.gedangan.m085_server
if errorlevel 1 pause
