from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget,QMessageBox
import os
import glob
import ctypes
from config import WALLPAPER_DIR

def set_wallpaper(image_path):
    print(image_path)
    if os.path.exists(image_path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    else:
        QMessageBox.critical(None, "Error", "Wallpaper file not found.")

class WallpaperChangerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wallpaper Changer")
        self.setGeometry(100, 100, 840, 640)

        self.label = QLabel("Select a wallpaper theme or upload a custom one", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.upload_button = QPushButton("Upload Custom Wallpaper", self)
        self.upload_button.clicked.connect(self.upload_wallpaper)

        self.theme_button = QPushButton("Choose Theme", self)
        self.theme_button.clicked.connect(self.choose_theme)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.theme_button,stretch=2)
        self.setLayout(layout)

        self.apply_stylesheet("styles.qss")

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