@echo off
echo Installing build requirements...
cmd /c pip install pyinstaller psutil PyQt6 requests

echo Building Stable Diffusion Launcher...
cmd /c pyinstaller --noconfirm --onefile --windowed ^
    --icon="%~dp0\webui.ico" ^
    --add-data "%~dp0\webui.ico;." ^
    --name "StableDiffusion" ^
    "%~dp0\sd_launcher.py"

echo Build complete! Executable is in the dist folder.
pause
