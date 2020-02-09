# Finnish Meteorological Institute Weather
Library for fetching weather information from
[Finnish Meteorological Institute (FMI)](https://en.ilmatieteenlaitos.fi/open-data). 

Originally build for personal use because I wanted to create a FMI integration for
[Home Assistant](https://www.home-assistant.io/).

Library is not yet available in [PyPi](https://pypi.org/).

## How to use

Working example can be found in [example.py](example.py). If there is a problem parsing the response or FMI service
returns an exception response, an exception is throws. It is up to the caller to handle the exceptions.

#### Get the weather using a place name

Selected station depends on FMI service but in general it should be the closest one and provide the latest measurements.
```python
import fmi_weather

weather = fmi_weather.weather_by_place_name("Mäkkylä, Espoo")
```

#### Get the weather using coordinates

FMI does not provide an easy way to get the the closest weather station by coordinates. A bounding box is used instead
since FMI returns all weather stations inside the box. The closest one to coordinates is selected, but
currently there is no check verifying what kind of station it is.

```python
import fmi_weather

weather = fmi_weather.weather_by_coordinates(63.361604, 27.392607)
```

#### Weather data
Depending on the weather station the following information is available:
- Station name
- Station latitude
- Station longitude
- Measurement time
- Temperature (°C)
- Humidity (%)
- Wind speed (m/s)
- Wind gust (m/s)
- Wind direction (°)
- Dew point (°C)
- Precipitation amount (mm)
- Precipitation intensity (mm/h)
- Pressure (hPa)
- Visibility (m)
- Cloud coverage (1/8)

Measurement data contains two fields: `value` and `unit`. You can also just print the measurement object to get a string
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
