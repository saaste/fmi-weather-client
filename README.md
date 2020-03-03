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

### Get weather and forecasts

```python
import fmi_weather_client

weather1 = fmi_weather_client.weather_by_coordinates(60.170998, 24.941325)
weather2 = fmi_weather_client.weather_by_place_name("Rastila, Helsinki")
forecast1 = fmi_weather_client.forecast_by_place_name("Jäppilä, Pieksämäki")
forecast2 = fmi_weather_client.forecast_by_coordinates(67.6894, 28.62406, timestep_hours=12)
```

There are also asynchronous versions available:
```python
weather1 = await fmi_weather_client.async_weather_by_coordinates(60.170998, 24.941325)
weather2 = await fmi_weather_client.async_weather_by_place_name("Rastila, Helsinki")
forecast1 = await fmi_weather_client.async_forecast_by_place_name("Jäppilä, Pieksämäki")
forecast2 = await fmi_weather_client.async_forecast_by_coordinates(67.6894, 28.62406, timestep_hours=12)
```

If data is not available, the following exception is thrown:
```
fmi_weather_client.errors.NoWeatherDataError
```

### Weather data
FMI provides the following commonly used information:
- Temperature (°C)
- Pressure (hPa)
- Humidity (%)
- Wind direction (°)
- Wind speed (m/s)
- Wind gust (m/s)
- Dew point (°)
- Cloud coverage (%)
- Precipitation intensity (mm/h)
- Symbol [Documentation in Finnish](https://www.ilmatieteenlaitos.fi/latauspalvelun-pikaohje)


There are also other information available. Check [models.py](fmi_weather_client/models.py) and FMI documentation for
more info.

## Development

### Setup
Create and activate a virtual environment
```
$ python -m venv venv
$ source venv/bin/activate
```

Install required packages
```
$ make setup-dev-env
```

Deactivate virtual environment when you are done
```
$ deactivate
```

### Run tests
This will run unit tests and code quality checks
```
$ make test
```
