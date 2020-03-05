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
You can get the weather using the following functions:
- `weather_by_place_name(place_name)`
- `weather_by_coordinates(latitude, longitude)`

Example:
```python
import fmi_weather_client as fmi
from fmi_weather_client.errors import ClientError, ServerError

try:
    weather = fmi.weather_by_place_name("Jäppilä, Pieksämäki")
    if weather is not None:
        print(f"Temperature in {weather.place} is {weather.data.temperature}")
except ClientError as err:
    print(f"Client error with status {err.status_code}: {err.message}")
except ServerError as err:
    print(f"Server error with status {err.status_code}: {err.body}")
```

You can get the forecasts using the following functions:
- `forecast_by_place_name(place_name, [timestep_hours=24])`
- `forecast_by_coordinates(latitude, longitude, [timestep_hours=24])`

Example:
```python
import fmi_weather_client as fmi
from fmi_weather_client.errors import ClientError, ServerError

try:
    forecast = fmi.forecast_by_coordinates(60.170998, 24.941325)
    for weather_data in forecast.forecasts:
        print(f"Temperature at {weather_data.time}: {weather_data.temperature}")
except ClientError as err:
    print(f"Client error with status {err.status_code}: {err.message}")
except ServerError as err:
    print(f"Server error with status {err.status_code}: {err.body}")

```

All functions have asynchronous versions available with `async_` prefix.

### Errors

##### ClientError
Happens if FMI service returns `400-499`. This can happens for example if:
- Provided coordinates are invalid
- Provided place is not recognized
- Weather data is not available

Error object contains status code and human-readable error message from FMI service.

##### ServerError
Happens if FMI service returns any other error.

Error object contains status code and raw response body from FMI service


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
