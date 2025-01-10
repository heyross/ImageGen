@echo off
echo Initializing new git repository...

:: Remove existing git information
rmdir /S /Q .git
del /F /Q .gitattributes .gitignore .gitmodules 2>nul

:: Initialize new git repository
git init

:: Create new .gitignore
echo Creating .gitignore...
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo build/
echo develop-eggs/
echo dist/
echo downloads/
echo eggs/
echo .eggs/
echo lib/
echo lib64/
echo parts/
echo sdist/
echo var/
echo wheels/
echo *.egg-info/
echo .installed.cfg
echo *.egg
echo MANIFEST
echo 
echo # Virtual Environment
echo venv/
echo ENV/
echo env/
echo 
echo # IDEs
echo .idea/
echo .vscode/
echo *.swp
echo 
echo # Stable Diffusion specific
echo models/
echo outputs/
echo embeddings/
echo .env
echo *.ckpt
echo *.safetensors
echo *.pth
echo logs/
echo 
echo # Windows
echo Thumbs.db
echo ehthumbs.db
echo Desktop.ini
echo $RECYCLE.BIN/
echo *.cab
echo *.msi
echo *.msm
echo *.msp
echo *.lnk
) > .gitignore

:: Create README.md if it doesn't exist in root
if not exist README.md (
    echo Creating root README.md...
    (
    echo # Enhanced Stable Diffusion Windows GUI
    echo.
    echo A customized version of Stable Diffusion WebUI with an optimized Windows native interface.
    echo.
    echo ## Features
    echo.
    echo - Automatic hardware detection and optimization
    echo - Native Windows GUI client
    echo - Combined launcher for both server and client
    echo - System-specific configurations for optimal performance
    echo - Easy to use interface with all major Stable Diffusion features
    echo.
    echo ## System Requirements
    echo.
    echo - Windows 10 or later
    echo - NVIDIA GPU with 6GB+ VRAM ^(8GB+ recommended^)
    echo - 16GB+ System RAM ^(32GB+ recommended^)
    echo - Python 3.10 or later
    echo.
    echo ## Installation
    echo.
    echo 1. Clone this repository
    echo 2. Run `build_all.bat` to:
    echo    - Detect your system configuration
    echo    - Apply optimized settings
    echo    - Build the standalone executable
    echo 3. Run `StableDiffusion.exe` to start both server and client
    echo.
    echo ## Configuration
    echo.
    echo The system automatically detects and configures for your hardware:
    echo - GPU memory optimization
    echo - CPU thread allocation
    echo - RAM usage optimization
    echo.
    echo ## License
    echo.
    echo MIT License
    ) > README.md
)

:: Add all files
git add .

:: Initial commit
git commit -m "Initial commit: Enhanced Stable Diffusion Windows GUI"

echo Repository initialized successfully!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub
echo 2. Run these commands to push your code:
echo    git remote add origin YOUR_GITHUB_REPO_URL
echo    git push -u origin main
echo.
pause
