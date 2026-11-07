@echo off
setlocal
cd /d "%~dp0"
rem Run offline precompute separately from interactive jobs; every stage is sequential.
for %%M in (m07_scenarios m07_projection m07_runner) do (
 ".venv\Scripts\python.exe" -m backend.gedangan.%%M
 if errorlevel 1 exit /b 1
)
".venv\Scripts\python.exe" -m backend.gedangan.m07_validation --sensitivity
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m07_validation
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m backend.gedangan.m07_reporting
if errorlevel 1 exit /b 1
".venv\Scripts\python.exe" -m unittest discover -s tests -v > documentation\m07\final-regression.txt 2>&1
if errorlevel 1 exit /b 1
pushd frontend
call npx tsc --noEmit > ..\documentation\m07\typescript.txt 2>&1
if errorlevel 1 (popd & exit /b 1)
call npx vite build --config vite.projection.config.ts > ..\documentation\m07\production-build.txt 2>&1
if errorlevel 1 (popd & exit /b 1)
popd
".venv\Scripts\python.exe" -m backend.gedangan.m07_delivery
if errorlevel 1 exit /b 1
echo M07 conditional projection rebuild complete. M08 not started.
endlocal
