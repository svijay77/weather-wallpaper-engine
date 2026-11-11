import logging
import sys

from config.config import Config, ConfigError
from service.weather_handler import (
    WeatherService,
    WeatherSnapshot,
    WeatherServiceInitError,
    WeatherServiceNetworkError
)
from service.wallpaper_handler import DynamicWallpaperService, DynamicWallpaperServiceError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

logger = logging.getLogger(__name__)

def app() -> int:
    try:
        logger.info("hello")
        # initialize services
        config = Config()
        weather_service = WeatherService(config)
        wallpaper_service = DynamicWallpaperService(config)

        logger.info("successfully initialized all services!")

        # grab weather snapshot from OpenWeather
        weather: WeatherSnapshot = weather_service.get_weather()

        # set wallpaper via configured wallpaper service
        wallpaper_service.set_wallpaper(weather)
        logger.info("successfully set new wallpaper!")

        return 0

    # exception handling -- on any exception, exit program immediately and DO NOT change current wallpaper
    except ConfigError as e:
        logger.error(f"[Config]: please fix your configuration. {e}")
        return 1

    except WeatherServiceInitError as e:
        logger.error(f"[WeatherService] WeatherService could not be initialized. {e}")
        return 1

    except WeatherServiceNetworkError as e:
        logger.warning(f"[WeatherService] weather status could not be fetched. {e}")
        return 0

    except DynamicWallpaperServiceError as e:
        logger.error(f"[DynamicWallpaperService] failed to set wallpaper. {e}")
        return 1

    except Exception:
        logger.exception("unknown error occurred")
        return 1

def main():
    sys.exit(app())

if __name__ == "__main__":
    main()
