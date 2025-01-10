import sys
import os
import json
import psutil
import subprocess
import nvidia_smi

def get_gpu_info():
    try:
        nvidia_smi.nvmlInit()
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
        info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
        name = nvidia_smi.nvmlDeviceGetName(handle)
        vram_total = info.total / (1024**3)  # Convert to GB
        return {
            "name": name.decode() if isinstance(name, bytes) else name,
            "vram": vram_total,
            "vendor": "NVIDIA"
        }
    except Exception as e:
        print(f"Error getting GPU info: {e}")
        return None

def get_system_info():
    cpu_info = {
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "name": ""
    }
    
    # Get CPU name on Windows
    try:
        output = subprocess.check_output("wmic cpu get name", shell=True).decode()
        cpu_info["name"] = output.split("\n")[1].strip()
    except:
        cpu_info["name"] = "Unknown CPU"

    ram_gb = psutil.virtual_memory().total / (1024**3)
    
    return {
        "cpu": cpu_info,
        "ram": ram_gb,
        "gpu": get_gpu_info()
    }

def optimize_config(system_info):
    config = {
        "commandline_args": [],
        "env_vars": {}
    }
    
    gpu = system_info["gpu"]
    ram = system_info["ram"]
    cpu_threads = system_info["cpu"]["threads"]
    
    # Base configuration
    config["commandline_args"].append("--api")
    config["commandline_args"].append("--xformers")
    
    # GPU-specific optimizations
    if gpu:
        vram = gpu["vram"]
        if vram <= 6:
            config["commandline_args"].extend([
                "--medvram",
                "--opt-split-attention",
                "--no-half-vae"
            ])
        elif vram <= 8:
            config["commandline_args"].extend([
                "--medvram",
                "--opt-split-attention"
            ])
        elif vram <= 12:
            config["commandline_args"].append("--opt-split-attention")
    
    # CPU optimizations
    if cpu_threads > 8:
        config["commandline_args"].append(f"--threads={cpu_threads-2}")  # Leave 2 threads for system
    
    # RAM optimizations
    if ram >= 64:
        config["env_vars"]["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb=128"
    
    return config

def main():
    system_info = get_system_info()
    config = optimize_config(system_info)
    
    # Save system info
    with open("system_info.json", "w") as f:
        json.dump(system_info, f, indent=2)
    
    # Save optimized config
    with open("optimized_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    # Print summary
    print("\nSystem Configuration:")
    print(f"CPU: {system_info['cpu']['name']} ({system_info['cpu']['cores']} cores, {system_info['cpu']['threads']} threads)")
    print(f"RAM: {system_info['ram']:.1f} GB")
    if system_info['gpu']:
        print(f"GPU: {system_info['gpu']['name']} ({system_info['gpu']['vram']:.1f} GB VRAM)")
    
    print("\nOptimized Configuration:")
    print("Command line arguments:")
    for arg in config['commandline_args']:
        print(f"  {arg}")
    if config['env_vars']:
        print("\nEnvironment variables:")
        for key, value in config['env_vars'].items():
            print(f"  {key}={value}")

if __name__ == "__main__":
    main()
