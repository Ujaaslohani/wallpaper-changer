from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QPixmap,QMovie
import os,requests
import glob
from config import WALLPAPER_DIR
from utilities import set_wallpaper

class WallpaperChangerUI(QWidget):
    def __init__(self,data):
        super().__init__()

        self.data=data

        self.setWindowTitle("Wallpaper Changer")
        self.setGeometry(100, 100, 840, 640)

        # text
        self.label = QLabel("Select a wallpaper theme or upload a custom one", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # time 
        self.time_label = QLabel("Fetching Time...", self)
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)

        # location and temperature
        self.weather_label = QLabel("Fetching Weather...", self)
        self.weather_label.setAlignment(QtCore.Qt.AlignCenter)

        # Weather Animation
        self.weather_icon = QLabel(self)
        self.weather_icon.setAlignment(QtCore.Qt.AlignCenter)

        # upload window
        self.upload_button = QPushButton("Upload Custom Wallpaper", self)
        self.upload_button.clicked.connect(self.upload_wallpaper)

        # choose theme window
        self.theme_button = QPushButton("Choose Theme", self)
        self.theme_button.clicked.connect(self.choose_theme)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.theme_button)
        layout.addWidget(self.time_label)
        layout.addWidget(self.weather_label)
        layout.addWidget(self.weather_icon)
        self.setLayout(layout)

        self.apply_stylesheet("styles.qss")

        # Start timers to update time and weather
        self.update_time()
        self.update_weather()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every second

        self.weather_timer = QTimer(self)
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(60000)  # Update every minute

    def update_time(self):
        current_time=QTime.currentTime().toString("hh.mm A")
        self.time_label.setText(f"Current Time: {current_time}")

    def update_weather(self):
        """Update UI with new weather data dynamically"""
        if self.data:
            city = self.data["location"]["name"]
            country = self.data["location"]["country"]
            temp = self.data["current"]["temp_c"]
            condition = self.data["current"]["condition"]["text"]
            icon_url = "https:" + self.data["current"]["condition"]["icon"]

            # Update label
            self.weather_label.setText(f"{city}, {country} | {temp}°C | {condition}")

            # Load and display the weather icon dynamically
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(icon_url).content)
            self.weather_icon.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio))



    def apply_stylesheet(self,file_path):
        if os.path.exists(file_path):
            with open(file_path,"r") as f:
                self.setStyleSheet(f.read())
        else:
            print(f"Stylesheet '{file_path}' not found!")

    def upload_wallpaper(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Wallpaper", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            dest_path = os.path.join(WALLPAPER_DIR, "Custom", os.path.basename(file_path))
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(file_path, "rb") as src, open(dest_path, "wb") as dst:
                dst.write(src.read())
            set_wallpaper(dest_path)
            QtWidgets.QMessageBox.information(self, "Success", "Custom wallpaper uploaded successfully!")

    def choose_theme(self):
        themes = ["Konbini", "Default", "Custom"]
        theme, ok = QtWidgets.QInputDialog.getItem(self, "Select Theme", "Choose a theme:", themes, 0, False)
        if ok and theme:
            if theme=="Custom":
                latest_wallpaper=self.get_latest_wallpaper()
                if latest_wallpaper:
                    set_wallpaper(latest_wallpaper)
                    QtWidgets.QMessageBox.information(self, "Theme Selected", f"Selected theme: {theme}")
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "No custom wallpapers found. Please upload one first")
            else:
                QtWidgets.QMessageBox.information(self, "Theme Selected", f"Selected theme: {theme}")

    def get_latest_wallpaper(self):
        custom_wallpapers_dir=os.path.join(WALLPAPER_DIR,"Custom")
        image_files=glob.glob(os.path.join(custom_wallpapers_dir,"*.png")) + \
        glob.glob(os.path.join(custom_wallpapers_dir,"*.jpg")) + \
        glob.glob(os.path.join(custom_wallpapers_dir,"*.jpeg"))
        if not image_files:
            return None
        latest_wallpaper=max(image_files, key=os.path.getmtime)
        return latest_wallpaper