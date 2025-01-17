import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QComboBox, QHBoxLayout

class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OptiTracker")
        self.setGeometry(100, 100, 600, 400) 
        self.setStyleSheet("background-color: #2D2D2D; color: #ECF0F1;") 
        
        # Central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Splash screen layout
        self.splash_layout = QVBoxLayout()
        self.splash_label = QLabel("OptiTracker Logo", self)
        self.splash_label.setAlignment(Qt.AlignCenter)
        self.splash_label.setStyleSheet("font-size: 24px; color: #3498DB; padding: 20px;")
        self.start_button = QPushButton("Start", self)
        self.start_button.setStyleSheet("background-color: #2ECC71; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.start_button.clicked.connect(self.show_main_screen)
        self.splash_layout.addWidget(self.splash_label)
        self.splash_layout.addWidget(self.start_button)
        self.layout.addLayout(self.splash_layout)

        # Camera selection screen layout
        self.main_layout = QVBoxLayout()
        self.camera_label = QLabel("Select Camera", self)
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("font-size: 18px; color: #ECF0F1; padding: 10px;")
        self.camera_dropdown = QComboBox(self)
        self.camera_dropdown.addItem("Camera 1")
        self.camera_dropdown.addItem("Camera 2")
        self.start_camera_button = QPushButton("Start Camera", self)
        self.start_camera_button.setStyleSheet("background-color: #3498DB; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.start_camera_button.clicked.connect(self.start_camera)
        self.main_layout.addWidget(self.camera_label)
        self.main_layout.addWidget(self.camera_dropdown)
        self.main_layout.addWidget(self.start_camera_button)
        self.layout.addLayout(self.main_layout)

        # Camera feed layout
        self.camera_feed_layout = QVBoxLayout()
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.camera_feed_layout.addWidget(self.video_label)

        self.stop_button = QPushButton("Stop Camera", self)
        self.stop_button.setStyleSheet("background-color: #E67E22; color: white; font-size: 16px; padding: 10px; border-radius: 5px;")
        self.stop_button.clicked.connect(self.stop_camera)
        self.camera_feed_layout.addWidget(self.stop_button)

        # Timer for updating video feed
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.cap = None

    def show_main_screen(self):
        # Switch from splash screen to main screen
        self.splash_layout.setParent(None)
        self.layout.addLayout(self.main_layout)

    def start_camera(self):
        # Start camera feed
        self.cap = cv2.VideoCapture(0)  # Assuming camera 1 is the default
        if not self.cap.isOpened():
            print("Error: Camera not found.")
            return
        self.main_layout.setParent(None)
        self.layout.addLayout(self.camera_feed_layout)
        self.timer.start(30)  # Update frame every 30 ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame.")
            return

        # Convert the frame to QImage format for display in QLabel
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        # Display the frame in the QLabel
        self.video_label.setPixmap(pixmap)

    def stop_camera(self):
        # Stop the camera feed and return to main screen
        self.timer.stop()
        self.cap.release()
        self.camera_feed_layout.setParent(None)
        self.layout.addLayout(self.main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
