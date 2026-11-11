from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
import logging

from ipinfo import getHandler, Handler
from pyowm import OWM
from pyowm.commons.exceptions import APIRequestError, APIResponseError, UnauthorizedError
from pyowm.weatherapi30.weather import Weather
from pyowm.weatherapi30.weather_manager import WeatherManager

from config.config import Config

logger = logging.getLogger(__name__)

#### CONSTANTS ####
class TimeOfDay(StrEnum):
    DAWN = 'dawn'
    DUSK = 'dusk'
    DAY = 'day'
    NIGHT = 'night'

    @classmethod
    def from_raw_times(cls, current_time: datetime, sunrise: datetime, sunset: datetime):
        if (sunrise - current_time) <= timedelta(minutes=90) and current_time <= sunrise: # dawn = [sunrise - 90, sunrise]
            return cls.DAWN
        elif current_time >= sunset and (current_time - sunset) <= timedelta(minutes=90): # dusk = [sunset, sunset + 90]
            return cls.DUSK
        elif current_time >= sunrise and current_time <= sunset: # day = [sunrise, sunset]
           return cls.DAY
        else: # night = [0:00, sunrise] U [sunset, 24:00]
            return cls.NIGHT

class WeatherStatus(StrEnum):
    CLOUDS = 'clouds'
    RAINY = 'rain'
    CLEAR = 'clear'
    WINDY = 'windy'
    SNOWY = 'snow'

    # calm luh data massaging for reasonable statuses
    @classmethod
    def from_raw_weather(cls, raw_status: str, clouds: int, wind_speed: float):
        cleaned_status = raw_status.strip().lower()

        if cleaned_status in RAINY_CONDITIONS:
            return cls.RAINY
        if cleaned_status == cls.CLOUDS and clouds < 50: # if its not at least 50% cloudy you dont get your cloudy wallpaper >:)
            return cls.CLEAR
        if cleaned_status == cls.CLEAR and wind_speed > 15.0: # api doesn't send back windy so check wind speeds
            return cls.WINDY

        try:
            return cls(cleaned_status)
        except ValueError:
            return cls.CLOUDS # covers mist, fog, haze, smoke, etc its close enough
       
RAINY_CONDITIONS = {'rain', 'drizzle', 'thunderstorm'}

@dataclass(frozen=True)
class WeatherSnapshot:
    status: WeatherStatus
    time_of_day: TimeOfDay

class WeatherService:
    def __init__(self, config: Config):
        owm = OWM(config.OPEN_WEATHER_TOKEN)
        self.weather_manager: WeatherManager = owm.weather_manager()
        self.ipinfo: Handler = getHandler(config.IP_INFO_TOKEN)

        if not self.weather_manager:
            raise WeatherServiceInitError("Could not create WeatherManager")
        if not self.ipinfo:
            raise WeatherServiceInitError("Could not create IPInfoHandler")

    def get_weather(self) -> WeatherSnapshot: 
        loc_details = self.ipinfo.getDetails().details
        lat, lon = loc_details['loc'].split(",")

        try:
            obs = self.weather_manager.weather_at_coords(float(lat), float(lon))
        except UnauthorizedError as e:
            raise WeatherServiceInitError("invalid OpenWeather API token") from e
        except APIRequestError as e:
            raise WeatherServiceNetworkError(f"could not retrieve weather observation for latitude: {lat}, longitude: {lon}") from e
        except APIResponseError as e:
            raise WeatherServiceNetworkError(f"failed to parse response object for latitude: {lat}, longitude: {lon}") from e

        weather: Weather = obs.weather

        # get required times as DateTime objs in the local timezone (normally in UTC)
        current_time = datetime.now().astimezone()
        sunrise = weather.sunrise_time(timeformat='date').astimezone()
        sunset = weather.sunset_time(timeformat='date').astimezone()
        
        new_status = WeatherStatus.from_raw_weather(
            raw_status=weather.status, 
            clouds=weather.clouds, 
            wind_speed=weather.wind().get('speed', 0.0)
            )
        time_of_day = TimeOfDay.from_raw_times(current_time, sunrise, sunset)

        weather_snapshot = WeatherSnapshot(new_status, time_of_day)
        logger.info(f"current weather snapshot: {weather_snapshot}")

        return weather_snapshot

class WeatherServiceInitError(Exception):
    pass

class WeatherServiceNetworkError(Exception):
    pass