@echo off
echo Installing build requirements...
cmd /c pip install --upgrade pyinstaller psutil PyQt6 requests nvidia-smi

echo Building Stable Diffusion Launcher...
cmd /c pyinstaller --noconfirm --onefile --windowed ^
    --icon="%~dp0\webui.ico" ^
    --add-data "%~dp0\webui.ico;." ^
    --hidden-import=PyQt6 ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=requests ^
    --hidden-import=psutil ^
    --hidden-import=json ^
    --hidden-import=nvidia_smi ^
    --name "StableDiffusion" ^
    "%~dp0\sd_launcher.py"

if errorlevel 1 (
    echo Error: Build failed!
    pause
    exit /b 1
)

echo Build complete! Executable is in the dist folder.
pause
