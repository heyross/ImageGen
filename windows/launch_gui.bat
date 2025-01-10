@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.10 or later.
    pause
    exit /b 1
)

:: Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install requirements
echo Installing/Updating requirements...
pip install -r requirements.txt

:: Launch the GUI
echo Starting Stable Diffusion GUI...
python sd_gui.py

:: Deactivate virtual environment
deactivate
