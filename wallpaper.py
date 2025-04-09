import os
import ctypes
import threading
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox
from config import WALLPAPER_DIR
from ui import WallpaperChangerUI
from utilities import get_weather,set_wallpaper,change_wallpaper,get_time_of_day


def wallpaper_updater(ui):
    """Fetch weather every hour using updated UI location and update wallpaper & UI"""
    while True:
        weather_data = get_weather(ui.location)  
        if weather_data:
            ui.data = weather_data  
            ui.update_weather()    
            change_wallpaper(weather_data)  
        time.sleep(3600)  


def main():
    app = QApplication([])
    location, ok = QInputDialog.getText(None, "Location Input", "Enter your city or location:")
    
    if ok and location:
        initial_data = get_weather(location)
        ui = WallpaperChangerUI(initial_data,location)
        ui.show()

        # Start wallpaper updater in a separate thread
        updater_thread = threading.Thread(target=wallpaper_updater, args=(ui,), daemon=True)
        updater_thread.start()

        app.exec_()

if __name__ == "__main__":
    main()
