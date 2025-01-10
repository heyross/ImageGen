@echo off
echo Creating Stable Diffusion Launcher

:: Install required packages for system detection
echo Installing system detection requirements...
cmd /c pip install --upgrade pip
cmd /c pip install pyinstaller psutil PyQt6 requests nvidia-ml-py3

:: Create directories if they don't exist
if not exist "windows" mkdir windows
if not exist "dist" mkdir dist

:: Detect system configuration
echo Detecting system configuration...
cd windows
cmd /c python detect_system.py
if errorlevel 1 (
    echo Error detecting system configuration
    pause
    exit /b 1
)
cd ..

:: Update webui-user.bat with optimized settings
echo Updating configuration...
cmd /c python windows\update_config.py
if errorlevel 1 (
    echo Error updating configuration
    pause
    exit /b 1
)

:: Create icon
echo Creating application icon...
cd windows
cmd /c python create_ico.py
if errorlevel 1 (
    echo Error creating icon
    pause
    exit /b 1
)
cd ..

:: Build the executable
echo Building executable...
call build_launcher.bat
if errorlevel 1 (
    echo Error building executable
    pause
    exit /b 1
)

:: Move the executable to the root directory
echo Moving executable to root directory...
if exist "dist\StableDiffusion.exe" (
    if exist "StableDiffusion.exe" del /F /Q "StableDiffusion.exe"
    move /Y "dist\StableDiffusion.exe" "."
    if errorlevel 1 (
        echo Error moving executable
        pause
        exit /b 1
    )
)

:: Clean up build artifacts
if exist "build" rmdir /S /Q "build"
if exist "dist" rmdir /S /Q "dist"
if exist "StableDiffusion.spec" del /F /Q "StableDiffusion.spec"

echo Done! You can now run StableDiffusion.exe to start both the server and client.
echo System-specific optimizations have been applied based on your hardware.

:: Display system info and configuration if files exist
if exist "windows\system_info.json" (
    echo.
    echo System Information:
    type "windows\system_info.json"
) else (
    echo Warning: System information file not found
)

echo.
if exist "windows\optimized_config.json" (
    echo Configuration applied:
    type "windows\optimized_config.json"
) else (
    echo Warning: Configuration file not found
)

pause
