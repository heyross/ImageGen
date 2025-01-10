@echo off
echo Creating Stable Diffusion Launcher

:: Install required packages for system detection
echo Installing system detection requirements...
cmd /c pip install psutil nvidia-smi

:: Detect system configuration
echo Detecting system configuration...
cd windows
cmd /c python detect_system.py
cd ..

:: Update webui-user.bat with optimized settings
echo Updating configuration...
cmd /c python windows\update_config.py

:: Create icon
echo Creating application icon...
cd windows
cmd /c python create_ico.py
cd ..

:: Build the executable
echo Building executable...
call build_launcher.bat

:: Move the executable to the root directory
echo Moving executable to root directory...
move /Y "dist\StableDiffusion.exe" "."
rmdir /S /Q "build" "dist"
del /F /Q "StableDiffusion.spec"

echo Done! You can now run StableDiffusion.exe to start both the server and client.
echo System-specific optimizations have been applied based on your hardware.
type windows\system_info.json
echo.
echo Configuration applied:
type windows\optimized_config.json
pause
