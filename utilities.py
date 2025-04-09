import os,ctypes,requests
from config import API_KEY,WALLPAPER_DIR
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime

def get_weather(location):
    """Fetch weather data from API"""
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={location}"
    try:
        response = requests.get(url)
        print(response)
        data = response.json()
        print(data)
        if "error" in data:
            QMessageBox.critical(None, "Error", "Invalid location. Please try again.")
            return None
        return data
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to fetch weather data: {str(e)}")
        return None
    
def set_wallpaper(image_path):
    print(image_path)
    if os.path.exists(image_path):
        ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
    else:
        QMessageBox.critical(None, "Error", "Wallpaper file not found.")

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
