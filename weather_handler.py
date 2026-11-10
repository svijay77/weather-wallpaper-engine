import sys

from ipinfo import getHandler, Handler
from pyowm import OWM
from pyowm.weatherapi30 import weather_manager
from pyowm.utils import config
from pyowm.utils import timestamps

from config import Config

class WeatherService:
    weather_manager = None
    ipinfo = None

    def __init__(self, config: Config) -> tuple[WeatherManager, Handler]:
        owm = OWM(config.open_weather_token)
        self.weather_manager = owm.weather_manager()
        self.ipinfo = getHandler(config.ipinfo_token)

        if not self.weather_manager:
            raise WeatherServiceInitError("Could not create WeatherManager")
        if not self.ipinfo:
            raise WeatherServiceInitError("Could not create IPInfoHandler")

    def get_weather_status(self) -> str: 
        loc_details = self.ipinfo.getDetails().details
        lat, lon = loc_details['loc'].split(",")
        
        obs = self.weather_manager.weather_at_coords(float(lat), float(lon))

        if obs:
            return obs.weather.status
        else:
            raise WeatherServiceStatusError(f"Could not retrieve weather observation for latitude: {lat}, longitude: {lon}")

class WeatherServiceInitError(Exception):
    pass

class WeatherServiceStatusError(Exception):
    pass