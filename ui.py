from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget
import os
from config import WALLPAPER_DIR

class WallpaperChangerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wallpaper Changer")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel("Select a wallpaper theme or upload a custom one", self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.upload_button = QPushButton("Upload Custom Wallpaper", self)
        self.upload_button.clicked.connect(self.upload_wallpaper)

        self.theme_button = QPushButton("Choose Theme", self)
        self.theme_button.clicked.connect(self.choose_theme)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.theme_button)
        self.setLayout(layout)

    def upload_wallpaper(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Wallpaper", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            dest_path = os.path.join(WALLPAPER_DIR, "Custom", os.path.basename(file_path))
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(file_path, "rb") as src, open(dest_path, "wb") as dst:
                dst.write(src.read())
            QtWidgets.QMessageBox.information(self, "Success", "Custom wallpaper uploaded successfully!")

    def choose_theme(self):
        themes = ["Konbini", "Default", "Custom"]
        theme, ok = QtWidgets.QInputDialog.getItem(self, "Select Theme", "Choose a theme:", themes, 0, False)
        if ok and theme:
            QtWidgets.QMessageBox.information(self, "Theme Selected", f"Selected theme: {theme}")
