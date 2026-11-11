import sys

from pyowm import OWM
from pyowm.weatherapi30.weather import Weather

from config.config import Config, ConfigError
from weather_handler import WeatherService, WeatherServiceInitError, WeatherServiceStatusError
from wallpaper_handler import DynamicWallpaperService, DynamicWallpaperServiceError

def app() -> int:
    try:
        # initialize services
        config = Config()
        weather_service = WeatherService(config)

        # grab weather status and pull appropriate wallpaper
        weather: Weather = weather_service.get_weather()

        wallpaper_service = DynamicWallpaperService(weather, config)

        # set wallpaper via service
        wallpaper_service.set_wallpaper()
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

    except DynamicWallpaperServiceError as e:
        print(f"[DynamicWallpaperService] failed to set wallpaper. {e}")
        return 1

def main():
    sys.exit(app())

if __name__ == "__main__":
    main()