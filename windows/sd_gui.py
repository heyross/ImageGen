import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QLineEdit, 
                            QSpinBox, QComboBox, QTextEdit, QScrollArea,
                            QFileDialog, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage
import requests

class SDThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    
    def __init__(self, prompt, params):
        super().__init__()
        self.prompt = prompt
        self.params = params
        
    def run(self):
        try:
            url = "http://127.0.0.1:7860"
            payload = {
                "prompt": self.prompt,
                "steps": self.params["steps"],
                "width": self.params["width"],
                "height": self.params["height"],
                "cfg_scale": self.params["cfg_scale"],
                "sampler_name": self.params["sampler"]
            }
            
            response = requests.post(f"{url}/sdapi/v1/txt2img", json=payload)
            if response.status_code == 200:
                result = response.json()
                self.finished.emit(result["images"][0])
            else:
                self.finished.emit("")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            self.finished.emit("")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stable Diffusion Windows GUI")
        self.setMinimumSize(1200, 800)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Left panel for controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Prompt input
        prompt_label = QLabel("Prompt:")
        self.prompt_input = QTextEdit()
        self.prompt_input.setMaximumHeight(100)
        
        # Parameters
        params_widget = QWidget()
        params_layout = QVBoxLayout(params_widget)
        
        # Steps
        steps_layout = QHBoxLayout()
        steps_label = QLabel("Steps:")
        self.steps_input = QSpinBox()
        self.steps_input.setRange(1, 150)
        self.steps_input.setValue(20)
        steps_layout.addWidget(steps_label)
        steps_layout.addWidget(self.steps_input)
        
        # Size
        size_layout = QHBoxLayout()
        width_label = QLabel("Width:")
        self.width_input = QSpinBox()
        self.width_input.setRange(64, 2048)
        self.width_input.setValue(512)
        height_label = QLabel("Height:")
        self.height_input = QSpinBox()
        self.height_input.setRange(64, 2048)
        self.height_input.setValue(512)
        size_layout.addWidget(width_label)
        size_layout.addWidget(self.width_input)
        size_layout.addWidget(height_label)
        size_layout.addWidget(self.height_input)
        
        # CFG Scale
        cfg_layout = QHBoxLayout()
        cfg_label = QLabel("CFG Scale:")
        self.cfg_input = QSpinBox()
        self.cfg_input.setRange(1, 30)
        self.cfg_input.setValue(7)
        cfg_layout.addWidget(cfg_label)
        cfg_layout.addWidget(self.cfg_input)
        
        # Sampler
        sampler_layout = QHBoxLayout()
        sampler_label = QLabel("Sampler:")
        self.sampler_input = QComboBox()
        self.sampler_input.addItems(["Euler a", "Euler", "LMS", "Heun", "DPM2", "DPM2 a", 
                                   "DPM++ 2S a", "DPM++ 2M", "DPM++ SDE", "DPM fast", 
                                   "DPM adaptive", "LMS Karras", "DPM2 Karras", 
                                   "DPM2 a Karras", "DPM++ 2S a Karras", 
                                   "DPM++ 2M Karras", "DPM++ SDE Karras"])
        sampler_layout.addWidget(sampler_label)
        sampler_layout.addWidget(self.sampler_input)
        
        # Generate button
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.generate_image)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # Add all parameter widgets
        params_layout.addLayout(steps_layout)
        params_layout.addLayout(size_layout)
        params_layout.addLayout(cfg_layout)
        params_layout.addLayout(sampler_layout)
        
        # Add widgets to left panel
        left_layout.addWidget(prompt_label)
        left_layout.addWidget(self.prompt_input)
        left_layout.addWidget(params_widget)
        left_layout.addWidget(self.generate_btn)
        left_layout.addWidget(self.progress_bar)
        left_layout.addStretch()
        
        # Right panel for image display
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Image display
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(512, 512)
        self.image_label.setStyleSheet("QLabel { background-color: #f0f0f0; }")
        
        # Save button
        self.save_btn = QPushButton("Save Image")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setVisible(False)
        
        right_layout.addWidget(self.image_label)
        right_layout.addWidget(self.save_btn)
        
        # Add panels to main layout
        layout.addWidget(left_panel, 1)
        layout.addWidget(right_panel, 2)
        
        self.current_image = None
        
    def generate_image(self):
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        params = {
            "steps": self.steps_input.value(),
            "width": self.width_input.value(),
            "height": self.height_input.value(),
            "cfg_scale": self.cfg_input.value(),
            "sampler": self.sampler_input.currentText()
        }
        
        self.thread = SDThread(self.prompt_input.toPlainText(), params)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.process_result)
        self.thread.start()
    
    def update_progress(self, value):
        self.progress_bar.setValue(value)
    
    def process_result(self, image_data):
        if image_data:
            import base64
            import io
            from PIL import Image
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert PIL image to QPixmap
            img_data = image.convert("RGBA").tobytes("raw", "RGBA")
            qimg = QImage(img_data, image.width, image.height, QImage.Format.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimg)
            
            # Scale pixmap to fit label while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(self.image_label.size(), 
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            
            self.image_label.setPixmap(scaled_pixmap)
            self.current_image = image_bytes
            self.save_btn.setVisible(True)
        
        self.generate_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
    
    def save_image(self):
        if not self.current_image:
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            os.path.expanduser("~/Pictures"),
            "PNG Images (*.png);;All Files (*.*)"
        )
        
        if file_name:
            if not file_name.lower().endswith('.png'):
                file_name += '.png'
            
            with open(file_name, 'wb') as f:
                f.write(self.current_image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
