# weather-wallpaper-engine
dynamically sets a wallpaper based on time and weather. arose from a need to view all my beautiful wallpapers but make them make sense with what i'm seeing outside my window. currently supports native Windows utility or LivelyCU to set the wallpaper, *maybe possibly* will extend to WallpaperEngine idk yet.

## Usage Guide

1. first ensure you have the appropriate API tokens. this script requires two tokens: 
- OpenWeather: you can get this token for free from their site [here](https://home.openweathermap.org/api_keys): just make a free account
- IP Info: also a free token that you can grab from their [website](https://ipinfo.io/dashboard/lite). still debating if this is necessary cuz i feel like i could grab the location from the system somewhere.

2. next, you need to make sure you have the latest Python version installed and pip, and then install all the required librariess in `requirements.txt` with `pip install -r requirements.txt`.

3. after those are done: there are a couple environment variables you need to set. 
**note**: still a wip if i read these config vars via system environment, a config JSON, or as CLI args. for now its pulling from your environment

| Variable | Description |
| --- | --- | --- |
| WEATHER_TOKEN | the weather token u pulled from OpenWeather |
| IPINFO_TOKEN | the token pulled from the IP info API |
| WINDOWS | if you're gonna use the native windows system to set the wallpaper |
| LIVELYCU | if you're gonna use Lively to set the wallpaper |
| WALLPAPER_DIR | the absolute path to the folder storing all your beautiful wallpapers |

after all this is set, just make sure you give necessary permissions to the python script and execute it via py -m main. 

