@rem Project-local process environment only. No registry or persistent PATH changes.
@set "SUMO_HOME=%~dp0toolchain\sumo-win64-1.28.0"
@set "PATH=%SUMO_HOME%\bin;%PATH%"
@set "PYTHONPATH=%SUMO_HOME%\tools;%PYTHONPATH%"
@echo SUMO_HOME=%SUMO_HOME%
@echo Prepared toolchain only. Gedangan engine remains disconnected.
