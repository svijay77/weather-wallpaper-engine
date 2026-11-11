import sys
from datetime import datetime, timedelta

from pyowm import OWM
from pyowm.weatherapi30.weather import Weather

from config import Config, ConfigError
from weather_handler import WeatherService, WeatherServiceInitError, WeatherServiceStatusError
from wallpaper_handler import DynamicWallpaperService

def app() -> int:
    try:
        # initialize services
        config = Config()
        weather_service = WeatherService(config)
        wallpaper_service = DynamicWallpaperService(config)

        # grab weather status and pull appropriate wallpaper
        status = weather_service.get_weather()

        # select appropriate path to wallpaper
        wallpaper_filename = get_wallpaper(status)

        if not wallpaper_filename:
            raise FileNotFoundError("could not match wallpaper to weather")

        full_path = config.WALLPAPER_DIR + "/" + wallpaper_filename
        print(full_path)
        # execute setting wallpaper based on cli arg
        return 0

    except ConfigError as e:
        print(f"[Config]: please fix your configuration. {e}")
        return 1

    except WeatherServiceInitError as e:
        print(f"[WeatherService] WeatherService could not be initialized. {e}")
        return 1

    except WeatherServiceStatusError as e:
        print(f"[WeatherService] weather status could not be fetched. {e}")
        return 0

    except FileNotFoundError as e:
        print(f"[Main] could not set wallpaper. {e}")
        return 1

def main():
    sys.exit(app())

if __name__ == "__main__":
    main()