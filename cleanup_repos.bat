@echo off
echo Cleaning up embedded repositories...

:: Remove embedded repositories
git rm --cached extensions/SadTalker
git rm --cached extensions/facechain
git rm --cached extensions/sd-dynamic-prompts
git rm --cached extensions/sd-webui-controlnet
git rm --cached extensions/sd-webui-reactor
git rm --cached repositories/BLIP
git rm --cached repositories/generative-models
git rm --cached repositories/k-diffusion
git rm --cached repositories/stable-diffusion-stability-ai
git rm --cached repositories/stable-diffusion-webui-assets

:: Remove the actual directories
rmdir /S /Q extensions\SadTalker
rmdir /S /Q extensions\facechain
rmdir /S /Q extensions\sd-dynamic-prompts
rmdir /S /Q extensions\sd-webui-controlnet
rmdir /S /Q extensions\sd-webui-reactor
rmdir /S /Q repositories\BLIP
rmdir /S /Q repositories\generative-models
rmdir /S /Q repositories\k-diffusion
rmdir /S /Q repositories\stable-diffusion-stability-ai
rmdir /S /Q repositories\stable-diffusion-webui-assets

:: Commit the cleanup
git add .
git commit -m "Cleaned up embedded repositories"

echo Repositories cleaned up successfully!
echo.
echo Next steps:
echo 1. Create a new repository on GitHub
echo 2. Run these commands to push your code:
echo    git remote add origin YOUR_GITHUB_REPO_URL
echo    git push -u origin main
echo.
pause
