@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Python lokal proyek belum tersedia. Setup proyek perlu dipulihkan.
 pause
 exit /b 1
)
if not exist "frontend\dist-m09\presentation.html" (
 echo Build presentasi belum tersedia. Jalankan REBUILD_PRESENTATION_M09.bat.
 pause
 exit /b 1
)
if not exist "presentation_demo\m09\cache\catalog.json" (
 echo Rekaman presentasi belum tersedia. Jalankan REBUILD_PRESENTATION_M09.bat.
 pause
 exit /b 1
)
echo GEDANGAN TRAFFIC SIMULATOR - EXTREME STUDIOS
echo Memeriksa rekaman lokal. Dashboard akan dibuka otomatis.
echo Internet, Node, SUMO live, login dan perubahan firewall tidak diperlukan untuk demo.
echo Tutup dengan Ctrl+C atau tombol Tutup layanan M09 pada dashboard.
".venv\Scripts\python.exe" -m backend.gedangan.m09_server --open
if errorlevel 1 pause
