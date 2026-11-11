import json
from pathlib import Path

class Config:
    OPEN_WEATHER_TOKEN: str = None # pull this token for free from https://openweathermap.org/ 
    IP_INFO_TOKEN: str = None # pull this token for free from https://ipinfo.io/signup 

    # TODO: look into extending to WallpaperEngine?
    # choose only between native windows or LivelyCU to set the wallpaper
    WALLPAPER_SYSTEM = None

    WALLPAPER_DIR: str = None # the absolute path to the folder where all your wallpapers are saved

    def __init__(self):
        config_file = Path("config.py")
        with config_file.open(mode='r', encoding='utf-8') as config:
            cfg = json.load(config)

        self.OPEN_WEATHER_TOKEN = cfg.get('WEATHER_TOKEN') 
        self.IP_INFO_TOKEN = cfg.get('IPINFO_TOKEN') 
        self.WALLPAPER_SYSTEM = cfg.get('WALLPAPER_SYSTEM').strip().lower()
        self.WALLPAPER_DIR = cfg.get('WALLPAPER_DIR')

        # verify tokens are set
        if not self.OPEN_WEATHER_TOKEN:
            raise ConfigError("OpenWeather API token must be set")
        if not self.IP_INFO_TOKEN:
            raise ConfigError("IPInfo token must be set")

        # make sure a correct wallpaper app is set
        if not self.WALLPAPER_system or self.WALLPAPER_SYSTEM not in ['windows', 'lively']:
            raise ConfigError("wallpaper system must either be windows or lively")

        # make sure a folder got passed in 
        if not self.WALLPAPER_DIR:
            raise ConfigError("wallpaper directory must be set")

        # ensure that it is a valid folder
        if not Path(self.WALLPAPER_DIR).isdir():
            raise ConfigError("wallpaper directory must be valid")


class ConfigError(Exception):
    pass



