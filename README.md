# Finnish Meteorological Institute Weather
Library for fetching weather information from
[Finnish Meteorological Institute (FMI)](https://en.ilmatieteenlaitos.fi/open-data). 

Originally build for personal use because I wanted to create a FMI integration for
[Home Assistant](https://www.home-assistant.io/).

Library is not yet available in [PyPi](https://pypi.org/).

## How to use

Working example can be found in [example.py](example.py).

##### Get closest weather station
```python
import fmi_weather

closest_station = fmi_weather.get_closest_station(60.22, 24.83)
```

##### Get weather using a place name

Selected station depends on FMI service but it should be the closest.
```python
import fmi_weather

weather = fmi_weather.get_weather_by_place(place='Leppävaara, Espoo')
```

##### Get weather using a station ID

```python
import fmi_weather

closest_station = fmi_weather.get_closest_station(60.22, 24.83)
weather = fmi_weather.get_weather_by_station(station_id=closest_station.id)
```

##### Station information
The library uses only automated weather stations and ignores other station types. The following fields are available
if FMI provides them: 
- Name
- Region
- Country
- Latitude
- Longitude

##### Weather
Depending on the weather station the following fields are available
- Temperature (°C)
- Wind (m/s)
- Humidity (%)
- Dew point (°C)
- Precipitation (mm/h)
- Pressure (hPa)
- Visibility (km)
- Cloud coverage (1/8)


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
