# Stable Diffusion Windows GUI Client

A native Windows GUI client for Stable Diffusion Web UI, built with PyQt6.

## Features

- Clean, native Windows interface
- Real-time image generation
- Support for all major Stable Diffusion parameters:
  - Steps control
  - Image size adjustment
  - CFG Scale
  - Multiple samplers
- Image saving functionality
- Progress tracking
- Responsive UI

## Requirements

- Windows 10 or later
- Python 3.10 or later
- Stable Diffusion Web UI running locally

## Installation

1. Make sure you have Python 3.10 or later installed
2. Run `launch_gui.bat` - it will:
   - Create a virtual environment
   - Install required dependencies
   - Launch the GUI application

## Usage

1. Start the Stable Diffusion Web UI with API access enabled
2. Launch this GUI client using `launch_gui.bat`
3. Enter your prompt and adjust parameters
4. Click "Generate" to create images
5. Use "Save Image" to save your generations

## System Requirements

Recommended:
- 8GB+ VRAM GPU (NVIDIA RTX 3060 Ti or better)
- 16GB+ System RAM
- Windows 10 or later

## Note

This GUI client requires the Stable Diffusion Web UI to be running with API access enabled. Make sure to start the Web UI with the `--api` parameter.
