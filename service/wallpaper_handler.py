import ctypes
import logging
from pathlib import Path
import random
import subprocess
import tempfile

import cv2

from config.config import Config
from service.weather_handler import WeatherSnapshot

logger = logging.getLogger(__name__)

# constants
SPI_SETDESKWALLPAPER = 20

WINDOW_EXTS = {'.png', '.jpg', '.jpeg', '.bmp'}
LIVELY_EXTS = {'.bmp','.webp','.png','.jpg','.jpeg','.mp4','.webm','.gif','.mkv','.avi','.mov','.wmv'}
VIDEO_EXTS = {'.mp4','.gif','.mkv','.avi','.mov','.wmv', '.webm'}

class DynamicWallpaperService:
    def __init__(self, config: Config):
        self.config: Config = config
        self.temp_frame_path = Path(tempfile.gettempdir()) / "dynamic_wallpaper_bridge.jpg"

        if config.WALLPAPER_SYSTEM == 'windows':
            self.allowed_exts: set[str] = WINDOW_EXTS
        elif config.WALLPAPER_SYSTEM == 'lively':
            self.allowed_exts: set[str] = LIVELY_EXTS

    def set_wallpaper(self, weather: WeatherSnapshot):
        wallpaper_file: Path = self.pick_wallpaper(weather)
        logger.info(f"successfully picked {str(wallpaper_file)} as the new wallpaper")

        logger.info(f"setting {str(wallpaper_file)} as wallpaper now...")

        match self.config.WALLPAPER_SYSTEM:
            case 'windows':
                logger.info("executing windows cmd...")
                ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, str(wallpaper_file), 3)
            case 'lively':
                # extracts first frame of next wallpaper if a video, and sets it via windows first to avoid screen flicker
                if wallpaper_file.suffix.lower() in VIDEO_EXTS:
                    if self.extract_first_frame(file=wallpaper_file):
                        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, str(self.temp_frame_path), 3)
                elif wallpaper_file.suffix.lower() in WINDOW_EXTS:
                    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, str(wallpaper_file), 3)

                logger.info("executing lively cmd...")
                self.run_command(['setwp', f'--file={str(wallpaper_file)}']) # TODO: add support for setting wallpapers only on certain monitors? i.e. only on monitor 1 or 2
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

        if len(files) < 1:
            raise DynamicWallpaperServiceError("no valid files exist")
        elif len(files) == 1:
            return files[0]
        
        return random.choice(files) # return one random choice from the list of matching files
    
    def extract_first_frame(self, file: Path) -> bool:
        video = cv2.VideoCapture(str(file)) # pylint: disable=no-member
        if not video.isOpened():
            raise DynamicWallpaperServiceError("failed to open wallpaper file")

        try:
            successful_read, frame = video.read()

            if successful_read:
                cv2.imwrite(self.temp_frame_path, frame)  # pylint: disable=no-member
                return True
            
            logger.warning("could not read first frame of wallpaper video")
            return False
        finally:
            video.release()

    def run_command(self, args):
        startup_info = subprocess.STARTUPINFO()
        startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run([self.config.LIVELY_PATH] + args, 
                       creationflags=subprocess.CREATE_NO_WINDOW, 
                       startupinfo=startup_info,
                       check=True
                       )

class DynamicWallpaperServiceError(Exception):
    pass
