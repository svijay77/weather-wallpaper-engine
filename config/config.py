import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class Config:
    OPEN_WEATHER_TOKEN: str # pull this token for free from https://openweathermap.org/ 
    IP_INFO_TOKEN: str # pull this token for free from https://ipinfo.io/signup 

    # TODO: look into extending to WallpaperEngine?
    # choose only between native windows or LivelyCU to set the wallpaper
    WALLPAPER_SYSTEM: str

    WALLPAPER_DIR: Path # the absolute path to the folder where all your wallpapers are saved
    LIVELY_PATH: Path

    def __init__(self):
        config_file = Path("./config/config.json")

        try:
            with config_file.open(mode='r', encoding='utf-8') as config:
                cfg = json.load(config)
        except FileNotFoundError as e:
            raise ConfigError("config file could not be found") from e
        except json.JSONDecodeError as e:
            raise ConfigError("config file JSON could not be decoded") from e
        if not isinstance(cfg, dict):
            raise ConfigError("malformed JSON")
        
        self.OPEN_WEATHER_TOKEN = cfg.get('WEATHER_TOKEN') 
        self.IP_INFO_TOKEN = cfg.get('IPINFO_TOKEN') 
        self.WALLPAPER_SYSTEM = cfg.get('WALLPAPER_SYSTEM').strip().lower() if cfg.get('WALLPAPER_SYSTEM') else None
        self.WALLPAPER_DIR = Path(cfg.get('WALLPAPER_DIR'))
        self.LIVELY_PATH = Path(cfg.get("LIVELY_PATH"))
  
        # verify tokens are set
        if not self.OPEN_WEATHER_TOKEN:
            raise ConfigError("OpenWeather API token must be set")
        if not self.IP_INFO_TOKEN:
            raise ConfigError("IPInfo token must be set")

        # make sure a correct wallpaper app is set
        if not self.WALLPAPER_SYSTEM or self.WALLPAPER_SYSTEM not in ['windows', 'lively']:
            raise ConfigError("wallpaper system must either be windows or lively")

        # make sure a folder got passed in 
        if not self.WALLPAPER_DIR:
            raise ConfigError("wallpaper directory must be set")

        # ensure that it is a valid folder
        if not self.WALLPAPER_DIR.is_dir():
            raise ConfigError("wallpaper directory must be valid")

        # ensure there's a valid path to the lively executable
        if not self.LIVELY_PATH.is_file():
            raise ConfigError("lively.exe path must be valid")

class ConfigError(Exception):
    pass



