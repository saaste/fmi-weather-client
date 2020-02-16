![Test](https://github.com/saaste/fmi-weather-client/workflows/tests/badge.svg?branch=master)
![Last commit](https://img.shields.io/github/last-commit/saaste/fmi-weather-client)
![Latest version in GitHub](https://img.shields.io/github/v/release/saaste/fmi-weather-client?include_prereleases)
![Latest version in PyPi](https://img.shields.io/pypi/v/fmi-weather-client)

# Finnish Meteorological Institute Weather
Library for fetching weather information from
[Finnish Meteorological Institute (FMI)](https://en.ilmatieteenlaitos.fi/open-data). 

Originally build for personal use because I wanted to create FMI integration for
[Home Assistant](https://www.home-assistant.io/).

**BETA WARNING!** This is still under heavy development. The public API is not frozen yet so DO NOT consider it to be
stable. Any version can have breaking changes. 

## How to use

Working example can be found in [example.py](example.py).

### Install

```
$ pip install fmi-weather-client 
```

### Get a weather by place name

```python
import fmi_weather_client

weather = fmi_weather_client.weather_by_place_name("Mäkkylä, Espoo")
```

Selected weather station depends on FMI service. Be aware, that sometimes FMI service does pretty poor job at selecting
a station that provides meaningful data. For example, at the time of writing weather from `Sipoo` returns data from
a station that measures cloud coverage and nothing more. Another example is `Kaivopuisto, Helsinki` which returns data
from a station that seems to be unavailable or broken.

If place name is not known or weather data is not available, the following exception is thrown:
```
fmi_weather_client.errors.NoWeatherDataError
```

### Get a weather by coordinates

```python
import fmi_weather_client

weather = fmi_weather_client.weather_by_coordinates(63.361604, 27.392607)
```

Returned data is from the closest weather station. Just like with place name search, station might return very little
data or nothing at all. If there are no stations within 90 km or weather data is not available, the following exception
is thrown:
```
fmi_weather_client.errors.NoWeatherDataError
```

### Get a combination weather

```python
import fmi_weather_client

weather = fmi_weather_client.weather_multi_station(69.016989, 21.465569)
```

Returned data is combination of multiple stations. Closest station is checked first and
if some variables are missing, next station is checked. This way it is likely to get all
variables it is possible that some data comes from a station that is quite far away. 

Returned station name and observation time is always the closest station. If there are no stations within 90 km or
weather data is not available, the following exception is thrown:
```
fmi_weather_client.errors.NoWeatherDataError
```

### Get a forecast
You can get the forecast using a place name or coordinates and the behaviour is the same. The code tries to fetch
the forecast for the next 6 days but looks like FMI provides it only for the next 3. You can also
define the timestep between forecasts. Default is 24 hours.

```python
forecast = fmi_weather_client.forecast_by_place_name("Jäppilä, Pieksämäki")
forecast2 = fmi_weather_client.forecast_by_coordinates(28.62406, 67.6894, timestep_hours=12)
```

### Weather data
Available weather information depends on the weather station. Currently supported fields: 
- Station name
- Station latitude
- Station longitude
- Observation time
- Temperature (°C)
- Humidity (%)
- Wind speed (m/s)
- Wind gust (m/s)
  - Maximum gust wind in the past 10 minutes
- Wind direction (°)
- Dew point (°C)
- Precipitation amount (mm)
  - Amount of rain in the past hour
- Precipitation intensity (mm/h)
- Pressure (hPa)
- Visibility (m)
- Cloud coverage
  - Cloud coverage is indicated as 1/8 sky.
  - 0.0 means no clouds
  - 4.0 means half cloudy
  - 8.0 means overcast
- Snow depth (cm)
- Current weather as WaWa code ([Documentation in Finnish](https://www.ilmatieteenlaitos.fi/latauspalvelun-pikaohje))

Observation data contains two fields: `value` and `unit`. You can also just print the observation object to get a string
representation:
```python
print('Temperature: %s' % weather.temperature)

# Output: Temperature: 1.4 °C
```

### Forecast data
- Geopotential height (m)
- Temperature (°C)
- Pressure (hPa)
- Humidity (%)
- Wind direction (°)
- Wind speed (m/s)
- Wind U component (m/s)
- Wind V component (m/s)
- Wind max (m/s)
- Wind gust (m/s)
- Dew point (°)
- Cloud cover (%)
- Symbol [Documentation in Finnish](https://www.ilmatieteenlaitos.fi/latauspalvelun-pikaohje)
- Precipitation amount 1h (mm/h)
- Precipitation amount (mm)

There are also other data regarding cloud coverage, radiation and land-sea mask. I have no idea
what these really are so it is best to check FMI documentation. 

## Development

### Setup
Create and activate a virtual environment
```
$ python -m venv venv
$ source venv/bin/activate
```

Install required packages
```
$ python -m pip install -r requirements.txt
$ python -m pip install -r requirements-dev.txt
```

When you stop working, deactivate virtual environment
```
$ deactivate
```

### Run tests
```
$ pytest
```

### Run code quality tools
```
$ flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude venv
$ flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127  --exclude venv
```
