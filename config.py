from dotenv import dotenv_values

class Config:
    OPEN_WEATHER_TOKEN: str = None # pull this token for free from https://openweathermap.org/ 
    IP_INFO_TOKEN: str = None # pull this token for free from https://ipinfo.io/signup 

    # TODO: look into extending to WallpaperEngine?
    # choose if you're gonna use native windows or LivelyCU to set the wallpaper
    IS_WINDOWS: bool = None
    IS_LIVELY_CU: bool = None

    WALLPAPER_DIR: str = None # the absolute path to the folder where all your wallpapers are saved

    def __init__(self):
        cfg = dotenv_values(".env")
        # TODO: pull config from JSON or CLI args? probably json tbh
        self.OPEN_WEATHER_TOKEN = cfg.get('WEATHER_TOKEN') 
        self.IP_INFO_TOKEN = cfg.get('IPINFO_TOKEN') 
        self.IS_WINDOWS = cfg.get('WINDOWS').strip().lower() == "true" if cfg.get('WINDOWS') else None
        self.IS_LIVELY_CU = cfg.get('LIVELYCU').strip().lower() == "true" if cfg.get('LIVELYCU') else None
        self.WALLPAPER_DIR = cfg.get('WALLPAPER_DIR')

        # verify tokens are set
        if not self.OPEN_WEATHER_TOKEN:
            raise ConfigError("OpenWeather API token must be set")
        if not self.IP_INFO_TOKEN:
            raise ConfigError("IPInfo token must be set")

        # make sure a wallpaper app is set
        if not (self.IS_LIVELY_CU or self.IS_WINDOWS):
            raise ConfigError("at least one wallpaper service must be set")

        # make sure there's a valid folder with wallpaper images
        if not self.WALLPAPER_DIR:
            raise ConfigError("wallpaper directory must be set and valid")

class ConfigError(Exception):
    pass



