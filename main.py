import sys
from datetime import datetime, timedelta

from pyowm import OWM
from pyowm.weatherapi30.weather import Weather

from config import Config, ConfigError
from weather_handler import WeatherService, WeatherServiceInitError, WeatherServiceStatusError
from wallpaper_handler import DynamicWallpaperService

def match_weather(status: str, time_of_day: str):
    # random choice between all wallpapers that follow [status]_day[0-9].[mp4/gif]
    match status.lower():
        case 'clear': 
            return f"clear_{time_of_day}.mp4"
        case 'cloudy':
            return f"cloudy_{time_of_day}.mp4"
        case 'rainy': 
            return f"rainy_{time_of_day}.mp4"
        case 'snowy':
            return f"snowy_{time_of_day}.mp4"
        case 'windy': 
            return f"windy_{time_of_day}.mp4"
        case default:
            return None
        
def get_wallpaper(weather: Weather) -> str:
    current_time = weather.reference_time(timeformat='date').astimezone()
    sunrise = weather.sunrise_time(timeformat='date').astimezone()
    sunset = weather.sunset_time(timeformat='date').astimezone()
    status = weather.status

    # define dawn and dusk as [sunrise - 90, sunrise] and [sunset, sunset + 90]
    if (sunrise - current_time) <= timedelta(minutes=90) and current_time <= sunrise:
        # random choice between the dawn wallpapers e.g. dawn[0-9]*.[mp4/gif]
        return "dawn.mp4"
    elif current_time >= sunset and (current_time - sunset) <= timedelta(minutes=90):
        # random choice between dusk wallpapers e.g. dusk[0-9]*.[mp4/gif]
        return "dusk.mp4" 
    elif current_time >= sunrise and current_time <= sunset:
        return match_weather(status, "day")
    elif current_time >= sunset or current_time <= sunrise:
        return match_weather(status, "night")

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