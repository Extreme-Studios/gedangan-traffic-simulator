@echo off
setlocal
cd /d "%~dp0"
".venv\Scripts\python.exe" -m backend.gedangan.m08_workflow %* > documentation\m08\rebuild-log.txt 2>&1
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m08_delivery
if errorlevel 1 exit /b 1
echo M08 rebuild complete. Engineering and policy gates remain separate. M09 not started.
endlocal
