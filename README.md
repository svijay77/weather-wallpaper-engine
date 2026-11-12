# weather-wallpaper-engine
dynamically sets a wallpaper based on time and weather. this arose from a need to view all my beautiful wallpapers but also make them make sense with what i'm seeing outside my window. currently supports native Windows utility or Lively to set the wallpaper, *maybe possibly* will extend to WallpaperEngine idk yet.

## Usage Guide

1. first ensure you have the appropriate API tokens. this script requires two tokens:
   - OpenWeather: you can get this token for free from their site [here](https://home.openweathermap.org/api_keys): just make a free account
   - IP Info: also a free token that you can grab from their [website](https://ipinfo.io/dashboard/lite). still debating if this is necessary cuz i feel like i could grab the location from the system somewhere.
2. next, you need to make sure you have the latest Python version installed and pip, and then install all the required libraries in `requirements.txt` with `pip install -r requirements.txt`.
3. after those are done: there are a couple environment variables you need to set in `config/config.json`.

| Variable | Description |
| --- | --- |
| WEATHER_TOKEN | the weather token u pulled from OpenWeather |
| IPINFO_TOKEN | the token pulled from the IP info API |
| WALLPAPER_SYSTEM | either `windows` or `lively`. if u only have static wallpapers (PNG, JPG, BMP) i recommend windows, otherwise lively handles a lot more file types) |
| WALLPAPER_DIR | the absolute path to the folder storing all your beautiful wallpapers |

after all this is set, just make sure you give Windows necessary permissions for the python script and execute it via `py -m main`. 

currently this sets the wallpaper based on time and day. you will have to manually schedule this to run via Windows TaskScheduler. it supports all combinations of dawn, day, dusk, night x windy, snowy, rain, clear, and clouds.

## TODO
### base functionality
- set up script to run in Windows background
- look into doing the same for Mac?
- add graceful handling for setting closest possible wallpaper (i.e. if user doesn't load a dusk/clear wallpaper, to use whatever is in dusk, or whatever is in night/clear etc)
- get rid of pyOWM and ipInfo libs? swap to lightweight http req client

### user experience
- look into loading wallpapers via GUI (customTkinter)?
- stretch: ML model that classifies uploaded wallpapers automatically into weather and time splits

