@echo off

set PYTHON=C:\Users\Ross Brown\AppData\Local\Programs\Python\Python310\python.exe
set VENV_DIR=%~dp0%venv

if exist %VENV_DIR% (
    rmdir /s /q %VENV_DIR%
)

"%PYTHON%" -m venv %VENV_DIR%
call %VENV_DIR%\Scripts\activate.bat

"%PYTHON%" launch.py %*
if exist tmp/restart goto :skip_venv
pause
exit /b

:skip_venv
if [%ACCELERATE%] == ["True"] goto :accelerate
goto :launch

:accelerate
echo Checking for accelerate
set ACCELERATE="%VENV_DIR%\Scripts\accelerate.exe"
if EXIST %ACCELERATE% goto :accelerate_launch

:launch
"%PYTHON%" launch.py %*
if exist tmp/restart goto :skip_venv
pause
exit /b

:accelerate_launch
echo Accelerating
"%ACCELERATE%" launch --num_cpu_threads_per_process=6 launch.py
if exist tmp/restart goto :skip_venv
pause
exit /b

:show_stdout_stderr

echo.
echo exit code: %errorlevel%

for /f %%i in ("tmp\stdout.txt") do set size=%%~zi
if %size% equ 0 goto :show_stderr
echo.
echo stdout:
type tmp\stdout.txt

:show_stderr
for /f %%i in ("tmp\stderr.txt") do set size=%%~zi
if %size% equ 0 goto :show_stderr
echo.
echo stderr:
type tmp\stderr.txt

:endofscript

echo.
echo Launch unsuccessful. Exiting.
pause
