@echo off

set PYTHON=
set GIT=
set VENV_DIR=
set COMMANDLINE_ARGS=--xformers --medvram --opt-split-attention --opt-sub-quad-attention --no-half-vae

call webui.bat
