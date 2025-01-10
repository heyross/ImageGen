# ImageGen - Enhanced Stable Diffusion Windows GUI

A customized version of Stable Diffusion WebUI with an optimized Windows native interface and automatic hardware detection.

## Features

- 🖥️ Native Windows GUI client with modern interface
- 🚀 Automatic hardware detection and optimization
- 🎮 Combined launcher for both server and client
- ⚙️ System-specific configurations for optimal performance
- 🎨 All major Stable Diffusion features in a clean interface
- 🔧 Optimized for NVIDIA GPUs (Especially RTX 3060 Ti)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/heyross/ImageGen.git
cd ImageGen
```

2. Run `build_all.bat` - This will:
   - Detect your system configuration
   - Apply optimized settings for your hardware
   - Build the standalone executable

3. Run `StableDiffusion.exe` to start both server and client

## System Requirements

Recommended:
- Windows 10 or later
- NVIDIA GPU with 8GB+ VRAM (Optimized for RTX 3060 Ti)
- 16GB+ System RAM (32GB+ recommended)
- Python 3.10 or later

Minimum:
- Windows 10
- NVIDIA GPU with 6GB+ VRAM
- 8GB System RAM
- Python 3.10

## Hardware Optimization

The system automatically detects and configures for your hardware:

### GPU Memory Optimization
- ≤6GB VRAM: Maximum optimization (--medvram --opt-split-attention --no-half-vae)
- ≤8GB VRAM: Medium optimization (--medvram --opt-split-attention)
- ≤12GB VRAM: Light optimization (--opt-split-attention)
- >12GB VRAM: Performance mode

### CPU & RAM
- Automatic thread allocation based on CPU cores
- Memory allocation optimization based on available RAM
- Xformers memory efficient attention enabled by default

## Components

- `windows/sd_gui.py` - Native Windows GUI client
- `sd_launcher.py` - Combined server/client launcher
- `windows/detect_system.py` - Hardware detection and optimization
- `windows/update_config.py` - Configuration management

## Development

To contribute or modify:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Building from Source

1. Install Python 3.10 or later
2. Run `build_all.bat`
3. Find `StableDiffusion.exe` in the root directory

## License

MIT License - See LICENSE file for details

## Acknowledgments

Based on the Stable Diffusion WebUI project, enhanced with:
- Native Windows GUI
- Automatic hardware optimization
- Streamlined user experience
