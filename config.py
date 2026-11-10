# TODO: pull config tokens from JSON?
import os

class Config:
    open_weather_token = None
    ipinfo_token = None

    def __init__(self):
        self.open_weather_token = os.environ['WEATHER_TOKEN']
        self.ipinfo_token = os.environ['IPINFO_TOKEN']

        if not self.open_weather_token:
            raise ConfigError("OpenWeather API token must be set")
        if not self.ipinfo_token:
            raise ConfigError("IPInfo token must be set")

class ConfigError(Exception):
    pass


