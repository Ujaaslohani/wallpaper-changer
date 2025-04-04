import os
import ctypes
import threading
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox
from datetime import datetime
from config import WALLPAPER_DIR
from ui import WallpaperChangerUI
from utilities import get_weather,set_wallpaper

def get_time_of_day():
    """Determine the time of day for wallpaper selection"""
    hour = datetime.now().hour
    print(hour)
    if 5 <= hour < 16:
        return "Morning"
    elif 16 <= hour < 18:
        return "Afternoon"
    else:
        return "Night"


def change_wallpaper(weather_data):
    if not weather_data:
        return

    condition = weather_data["current"]["condition"]["text"].lower()
    time_of_day = get_time_of_day()

    wallpaper_map = {
                "clear": {
            "Morning": "Konbini_Day.jpg",
            "Evening": "Konbini_Sunset.jpg",
            "Night": "Konbini_Night.jpg",
        },
        "partly cloudy": "Konbini_Day_Cloudy.jpg",
        "cloudy": "Konbini_Day_Cloudy.jpg",
        "overcast": "Konbini_Day_Cloudy.jpg",
        "mist": "Konbini_Day_Foggy.jpg",
        "patchy rain possible": "Konbini_Rain.jpg",
        "light rain": "Konbini_Rain.jpg",
        "moderate rain": "Konbini_Rain.jpg",
        "heavy rain": "Konbini_Rain.jpg",
        "thundery outbreaks possible": "Konbini_Rain.jpg",
        "patchy light snow": "Konbini_Day_Foggy.jpg",
        "light snow": "Konbini_Day_Foggy.jpg",
        "moderate snow": "Konbini_Day_Foggy.jpg",
        "heavy snow": "Konbini_Day_Foggy.jpg",
        "fog": "Konbini_Day_Foggy.jpg",
        "freezing fog": "Konbini_Day_Foggy.jpg",
        "patchy light drizzle": "Konbini_Rain.jpg",
        "light drizzle": "Konbini_Rain.jpg",
        "freezing drizzle": "Konbini_Rain.jpg",
        "patchy light rain with thunder": "Konbini_Rain.jpg",
        "moderate or heavy rain with thunder": "Konbini_Rain.jpg",
        "patchy light snow with thunder": "Konbini_Day_Foggy.jpg",
        "moderate or heavy snow with thunder": "Konbini_Day_Foggy.jpg"
    }

    if condition == "clear":
        
        
        selected_wallpaper = wallpaper_map["clear"].get(time_of_day, "Konbini_Night.jpg")
    else:
        selected_wallpaper = wallpaper_map.get(condition, "Konbini_Day.jpg")

    wallpaper_path = os.path.join(WALLPAPER_DIR, "Assets", "Konbini", selected_wallpaper)
    set_wallpaper(wallpaper_path)


def wallpaper_updater(ui, location):
    """Fetch weather every hour and update wallpaper & UI"""
    while True:
        weather_data = get_weather(location)
        if weather_data:
            ui.update_weather()  # Update UI dynamically
            change_wallpaper(weather_data)  # Change wallpaper
        time.sleep(3600)  # Wait for an hour before updating again

def main():
    app = QApplication([])
    location, ok = QInputDialog.getText(None, "Location Input", "Enter your city or location:")
    
    if ok and location:
        initial_data = get_weather(location)
        ui = WallpaperChangerUI(initial_data)
        ui.show()

        # Start wallpaper updater in a separate thread
        updater_thread = threading.Thread(target=wallpaper_updater, args=(ui, location), daemon=True)
        updater_thread.start()

        app.exec_()

if __name__ == "__main__":
    main()
