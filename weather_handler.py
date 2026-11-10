import sys

from ipinfo import getHandler, Handler
from pyowm import OWM

from config import Config

class WeatherService:
    weather_manager = None
    ipinfo = None

    def __init__(self, config: Config) -> tuple[WeatherManager, Handler]:
        owm = OWM(config.OPEN_WEATHER_TOKEN)
        self.weather_manager = owm.weather_manager()
        self.ipinfo = getHandler(config.IP_INFO_TOKEN)

        if not self.weather_manager:
            raise WeatherServiceInitError("Could not create WeatherManager")
        if not self.ipinfo:
            raise WeatherServiceInitError("Could not create IPInfoHandler")

    def get_weather(self) -> str: 
        loc_details = self.ipinfo.getDetails().details
        lat, lon = loc_details['loc'].split(",")
        
        obs = self.weather_manager.weather_at_coords(float(lat), float(lon))

        if obs:
            return obs.weather
        else:
            raise WeatherServiceStatusError(f"Could not retrieve weather observation for latitude: {lat}, longitude: {lon}")

class WeatherServiceInitError(Exception):
    pass

class WeatherServiceStatusError(Exception):
    pass