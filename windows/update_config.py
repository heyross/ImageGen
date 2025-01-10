import json
import os
import re

def update_webui_user_bat(config):
    webui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'webui-user.bat')
    
    # Read current content
    with open(webui_path, 'r') as f:
        content = f.readlines()
    
    # Update or add environment variables
    env_vars_added = False
    for i, line in enumerate(content):
        if line.strip().startswith('set COMMANDLINE_ARGS='):
            content[i] = f'set COMMANDLINE_ARGS={" ".join(config["commandline_args"])}\n'
        elif line.strip().startswith('set ') and not env_vars_added:
            # Add new environment variables after existing ones
            for var, value in config['env_vars'].items():
                content.insert(i+1, f'set {var}={value}\n')
            env_vars_added = True
    
    # If no environment variables section found, add at the beginning
    if not env_vars_added and config['env_vars']:
        insert_pos = 0
        for var, value in config['env_vars'].items():
            content.insert(insert_pos, f'set {var}={value}\n')
            insert_pos += 1
    
    # Write back the updated content
    with open(webui_path, 'w') as f:
        f.writelines(content)

def main():
    try:
        # Load optimized configuration
        config_path = os.path.join(os.path.dirname(__file__), 'optimized_config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Update webui-user.bat
        update_webui_user_bat(config)
        print("Successfully updated webui-user.bat with optimized configuration")
        
    except Exception as e:
        print(f"Error updating configuration: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
