import ctypes
import logging
from pathlib import Path
import random
from subprocess import run

from config.config import Config
from service.weather_handler import WeatherSnapshot

logger = logging.getLogger(__name__)

# constants
SPI_SETDESKWALLPAPER = 20

WINDOW_EXTS = {'.png', '.jpg', '.jpeg', '.bmp'}
LIVELY_EXTS = {'.bmp','.webp','.png','.jpg','.jpeg','.mp4','.webm','.gif','.mkv','.avi','.mov','.wmv'}

class DynamicWallpaperService:
    def __init__(self, config: Config):
        self.config: Config = config

        if config.WALLPAPER_SYSTEM == 'windows':
            self.allowed_exts: set[str] = WINDOW_EXTS
        elif config.WALLPAPER_SYSTEM == 'lively':
            self.allowed_exts: set[str] = LIVELY_EXTS

    def set_wallpaper(self, weather: WeatherSnapshot):
        file: Path = self.pick_wallpaper(weather)
        logger.info(f"successfully picked {str(file)} as the new wallpaper")

        logger.info(f"setting {str(file)} as wallpaper now...")

        match self.config.WALLPAPER_SYSTEM:
            case 'windows':
                logger.info("executing windows cmd...")
                #ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, str(file), 3)
            case 'lively':
                logger.info("executing lively cmd...")
                #run(['setwp', f'--file={str(file)}']) # TODO: add support for setting wallpapers only on certain monitors? i.e. only on monitor 1 or 2
            case _:
                raise DynamicWallpaperServiceError('invalid wallpaper system')

    def pick_wallpaper(self, weather: WeatherSnapshot) -> Path:
        # the issue here is that im gonna have to make sure the directory structure always follows the same statuses available from OWM
        folder = Path(self.config.WALLPAPER_DIR) / weather.time_of_day / weather.status
        
        # check folder exists
        if not folder.is_dir():
            # if it doesn't exist, use the parent folder
            logger.warning(f"wallpaper folder does not exist: {folder}")
            folder = folder.parent

        file_paths = folder.iterdir()
        files = []

        # filter to only include files with valid extensions
        for path in file_paths:
            if path.is_file() and path.suffix.lower() in self.allowed_exts:
                files.append(path)
                logger.info(f"adding file: {str(path)}")

        if len(files) < 1:
            raise DynamicWallpaperServiceError("no valid files exist")
        elif len(files) == 1:
            return files[0]
        
        return random.choice(files) # return one random choice from the list of matching files

class DynamicWallpaperServiceError(Exception):
    pass
