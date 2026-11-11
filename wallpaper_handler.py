import ctypes
from datetime import timedelta
from enum import StrEnum
from pathlib import Path
from random import choice
from subprocess import runCommand

from pyowm.weatherapi30.weather import Weather

from config import Config

# constants
SPI_SETDESKWALLPAPER = 20

class TimeOfDay(StrEnum):
    DAWN = 'dawn'
    DUSK = 'dusk'
    DAY = 'day'
    NIGHT = 'night'

class DynamicWallpaperService:
    weather: Weather = None
    config: Config = None
    allowed_exts: list[str] = None

    def __init__(self, weather: Weather, config: Config):
        self.weather = weather
        self.config = config

        if config.WALLPAPER_SYSTEM == 'windows':
            allowed_exts = ['.png', '.jpg', '.jpeg', '.bmp']
        elif config.WALLPAPER_SYSTEM == 'lively':
            allowed_exts = ['.bmp','.webp','.png','.jpg','.jpeg','.mp4','.webm','.gif','.mkv','.avi','.mov','.wmv']

    def set_wallpaper(self):
        filename = self.pick_wallpaper()
        
        match self.config.WALLPAPER_SYSTEM:
            case 'windows':
                # execute via windows cmd
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, self.config.WALLPAPER_DIR, 3)
            case 'lively':
                runCommand(['setwp', f'--file={filename}']) # TODO: add support for setting wallpapers only on certain monitors? i.e. only on monitor 1 or 2
            case default:
                raise DynamicWallpaperServiceError('cannot set wallpaper due to unknown system')

    def pick_wallpaper(self) -> str:
        current_time = self.weather.reference_time(timeformat='date').astimezone()
        sunrise = self.weather.sunrise_time(timeformat='date').astimezone()
        sunset = self.weather.sunset_time(timeformat='date').astimezone()

        status = self.weather.status.lower()
        wind_speed = float(self.weather.wind()['speed'])
        
        time_of_day = None

        if (sunrise - current_time) <= timedelta(minutes=90) and current_time <= sunrise: # dawn = [sunrise - 90, sunrise]
            time_of_day = TimeOfDay.DAWN
        elif current_time >= sunset and (current_time - sunset) <= timedelta(minutes=90): # dusk = [sunset, sunset + 90]
            time_of_day = TimeOfDay.DUSK
        elif current_time >= sunrise and current_time <= sunset: # day = [sunrise, sunset]
            time_of_day = TimeOfDay.DAY
        elif current_time >= sunset or current_time <= sunrise: # night = [0:00, sunrise] U [sunset, 24:00]
            time_of_day = TimeOfDay.NIGHT

        return choice(self.match_weather(status, wind_speed, time_of_day)) # return one random choice from the list of matching files

    def match_weather(self, status: str, wind_speed: float, time_of_day: str) -> list[str]:
        # rain takes prio over wind speeds until i add a thunderstorm category?
        if status in ['thunderstorm', 'drizzle']: # not exactly the most robust handling of status tbh
            status = 'rain'
        elif wind_speed > 15.0: # there's no 'windy' descriptor in the API so i check wind speed
           status = 'windy'

        return self.get_all_matching_files(time_of_day=time_of_day, status=status) # the issue here is that im gonna have to make sure the directory structure always follows the same statuses available from OWM
       
    # returns all wallpapers inside WALLPAPER_DIR/{time_of_day}/{status}/*.[allowed_exts]
    def get_all_matching_files(self, time_of_day: str, status: str) -> list[str]:
        folder = Path(f'{self.config.WALLPAPER_DIR}/{time_of_day}/{status}')

class DynamicWallpaperServiceError(Exception):
    pass
