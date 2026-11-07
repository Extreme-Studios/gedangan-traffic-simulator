@echo off
setlocal
cd /d "%~dp0"
rem Rebuild only software experiments. Never reset or promote field observations.
for %%M in (m06_calibration m06_reproducibility m06_uncertainty m06_reporting) do (
  ".venv\Scripts\python.exe" -m backend.gedangan.%%M
  if errorlevel 1 exit /b 1
)
".venv\Scripts\python.exe" -m unittest discover -s tests -v > documentation\m06\final-regression.txt 2>&1
if errorlevel 1 exit /b 1
pushd frontend
call npx tsc --noEmit > ..\documentation\m06\typescript.txt 2>&1
if errorlevel 1 (popd & exit /b 1)
call npx vite build --config vite.calibration.config.ts > ..\documentation\m06\production-build.txt 2>&1
if errorlevel 1 (popd & exit /b 1)
popd
".venv\Scripts\python.exe" -m backend.gedangan.m06_delivery
if errorlevel 1 exit /b 1
echo M06 software rebuild complete. Empirical baseline remains blocked pending verified data and review.
endlocal
