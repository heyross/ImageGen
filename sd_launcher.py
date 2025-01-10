import os
import sys
import subprocess
import time
import requests
import threading
import psutil
from PyQt6.QtWidgets import QApplication, QProgressDialog, QMessageBox
from PyQt6.QtCore import Qt, QTimer

def is_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def check_server_status():
    try:
        response = requests.get("http://127.0.0.1:7860/sdapi/v1/sd-models")
        return response.status_code == 200
    except:
        return False

def start_server():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    webui_path = os.path.join(current_dir, 'webui-user.bat')
    
    # Add the --api parameter to enable the API
    with open(webui_path, 'r') as f:
        content = f.read()
    
    if '--api' not in content:
        content = content.replace('set COMMANDLINE_ARGS=', 'set COMMANDLINE_ARGS=--api ')
        with open(webui_path, 'w') as f:
            f.write(content)
    
    # Start the server
    subprocess.Popen([webui_path], 
                    cwd=current_dir,
                    creationflags=subprocess.CREATE_NEW_CONSOLE)

def start_client():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    client_path = os.path.join(current_dir, 'windows', 'launch_gui.bat')
    subprocess.Popen([client_path],
                    cwd=os.path.join(current_dir, 'windows'),
                    creationflags=subprocess.CREATE_NEW_CONSOLE)

class LauncherDialog(QProgressDialog):
    def __init__(self):
        super().__init__("Starting Stable Diffusion...", None, 0, 100)
        self.setWindowTitle("Stable Diffusion Launcher")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setMinimumDuration(0)
        self.setAutoClose(True)
        self.setAutoReset(False)
        
        self.setValue(0)
        self.server_started = False
        self.max_wait_time = 300  # 5 minutes timeout
        self.elapsed_time = 0
        
        # Start the server
        self.server_thread = threading.Thread(target=start_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        # Setup timer for progress updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_progress)
        self.timer.start(1000)  # Check every second

    def check_progress(self):
        self.elapsed_time += 1
        
        if check_server_status():
            self.setValue(100)
            self.timer.stop()
            QTimer.singleShot(500, self.start_client_application)
            return
            
        if self.elapsed_time >= self.max_wait_time:
            self.timer.stop()
            QMessageBox.critical(None, "Error", 
                               "Timeout waiting for Stable Diffusion server to start.\n"
                               "Please check the server console for errors.")
            self.close()
            return
            
        # Update progress based on elapsed time
        progress = min(95, (self.elapsed_time / self.max_wait_time) * 100)
        self.setValue(int(progress))
        
        # Update status message
        if self.elapsed_time < 10:
            self.setLabelText("Starting Stable Diffusion server...")
        elif self.elapsed_time < 30:
            self.setLabelText("Waiting for server initialization...")
        else:
            self.setLabelText("Loading models... This may take a few minutes.")

    def start_client_application(self):
        start_client()
        self.close()

def main():
    # Check if server is already running
    if check_server_status():
        response = QMessageBox.question(None, "Server Running",
                                      "Stable Diffusion server is already running.\n"
                                      "Would you like to start the client?",
                                      QMessageBox.StandardButton.Yes | 
                                      QMessageBox.StandardButton.No)
        
        if response == QMessageBox.StandardButton.Yes:
            start_client()
        return

    app = QApplication(sys.argv)
    launcher = LauncherDialog()
    launcher.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
