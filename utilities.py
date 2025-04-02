import os,ctypes,requests
from config import API_KEY
from PyQt5.QtWidgets import QMessageBox

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