![Test](https://github.com/saaste/fmi-weather-client/workflows/tests/badge.svg?branch=master)
![Last commit](https://img.shields.io/github/last-commit/saaste/fmi-weather-client)
![Latest version in GitHub](https://img.shields.io/github/v/release/saaste/fmi-weather-client)
![Latest version in PyPi](https://img.shields.io/pypi/v/fmi-weather-client)

# Finnish Meteorological Institute Weather
Library for fetching weather information from
[Finnish Meteorological Institute (FMI)](https://en.ilmatieteenlaitos.fi/open-data). 

Originally build for personal use because I wanted to create FMI integration for
[Home Assistant](https://www.home-assistant.io/).

## How to use

Working example can be found in [example.py](example.py).

### Install

```
$ pip install fmi-weather-client 
```

### Get the weather by place name

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

### Get the weather by coordinates

```python
import fmi_weather_client

weather = fmi_weather_client.weather_by_coordinates(63.361604, 27.392607)
```

Returned data is from the closest weather station. Just like with place name search, station might return very little
data or nothing at all. If there are no stations within 50 km or weather data is not available, the following exception
is thrown:
```
fmi_weather_client.errors.NoWeatherDataError
```


### Weather data
Available weather information depends on the weather station. Currently supported fields: 
- Station name
- Station latitude
- Station longitude
- Measurement time
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

Observation data contains two fields: `value` and `unit`. You can also just print the measurement object to get a string
representation:
```python
print('Temperature: %s' % weather.temperature)

# Output: Temperature: 1.4 °C
```


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
