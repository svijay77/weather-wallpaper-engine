import sys

from config import Config, ConfigError
from weather_handler import WeatherService, WeatherServiceInitError, WeatherServiceStatusError

def main():
    try:
        config = Config()
        weather_service = WeatherService(config)
        print(weather_service.get_weather_status())
    except ConfigError as e:
        print(f"[Config]: please fix your configuration. {e}")
        sys.exit(1)
    except WeatherServiceInitError as e:
        print(f"[WeatherService] WeatherService could not be initialized. {e}")
        sys.exit(1)
    except WeatherServiceStatusError as e:
        print(f"[WeatherService] weather status could not be fetched. {e}")

if __name__ == "__main__":
    main()