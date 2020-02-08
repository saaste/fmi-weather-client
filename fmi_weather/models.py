from typing import Optional
from datetime import datetime

class Station:
    def __init__(self,
                 station_id: int,
                 name: Optional[str] = None,
                 region: Optional[str] = None,
                 country: Optional[str] = None,
                 lat: Optional[float] = None,
                 lon: Optional[float] = None):
        self.id: int = station_id
        self.name: Optional[str] = name
        self.region: Optional[str] = region
        self.country: Optional[str] = country
        self.lat: float = lat
        self.lon: float = lon


class WeatherLocation:
    def __init__(self, name: str, lat: float, lon: float):
        self.name: str = name
        self.lat: float = lat
        self.lon: float = lon


# TODO: DEPRECATED
class WeatherMeasurement:
    def __init__(self, measurement_type: str, time: str, value: float):
        self.type: str = measurement_type
        self.time: str = time
        self.value: float = value

class NewWeatherMeasurement:
    def __init__(self, value: float, unit: str):
        self.value: float = value
        self.unit: str = unit


# TODO: DEPRECATED
class Weather:
    def __init__(self, location: WeatherLocation):
        self.location: WeatherLocation = location
        self.temperature: Optional[WeatherMeasurement] = None
        self.humidity: Optional[WeatherMeasurement] = None
        self.wind_speed: Optional[WeatherMeasurement] = None
        self.dew_point: Optional[WeatherMeasurement] = None
        self.precipitation: Optional[WeatherMeasurement] = None
        self.pressure: Optional[WeatherMeasurement] = None
        self.visibility: Optional[WeatherMeasurement] = None
        self.cloud_coverage: Optional[WeatherMeasurement] = None


class NewWeather:
    def __init__(self, location: WeatherLocation, measurement_time: datetime):
        self.location: WeatherLocation = location
        self.measurement_time = measurement_time
        self.temperature: Optional[NewWeatherMeasurement] = None
        self.humidity: Optional[NewWeatherMeasurement] = None
        self.wind_speed: Optional[NewWeatherMeasurement] = None
        self.wind_gust: Optional[NewWeatherMeasurement] = None
        self.wind_direction: Optional[NewWeatherMeasurement] = None
        self.dew_point: Optional[NewWeatherMeasurement] = None
        self.precipitation_amount: Optional[NewWeatherMeasurement] = None
        self.precipitation_intensity: Optional[NewWeatherMeasurement] = None
        self.snow_depth: Optional[NewWeatherMeasurement] = None
        self.pressure: Optional[NewWeatherMeasurement] = None
        self.visibility: Optional[NewWeatherMeasurement] = None
        self.cloud_coverage: Optional[NewWeatherMeasurement] = None
