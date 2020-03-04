from datetime import datetime
from typing import List, Optional, NamedTuple


class FMIPlace(NamedTuple):
    """Represent a place in FMI response"""
    name: str
    lat: float
    lon: float

    def __str__(self):
        return f"{self.name} ({self.lat}, {self.lon})"


class Value(NamedTuple):
    """Represents a weather value"""
    value: Optional[float]
    unit: str

    def __str__(self):
        return f"{self.value} {self.unit}"


class WeatherData(NamedTuple):
    """Represents a weather"""
    time: datetime
    temperature: Value
    dew_point: Value
    pressure: Value
    humidity: Value
    wind_direction: Value
    wind_speed: Value
    wind_u_component: Value
    wind_v_component: Value
    wind_max: Value  # Max 10 minutes average
    wind_gust: Value  # Max 3 seconds average
    symbol: Value
    cloud_cover: Value
    cloud_low_cover: Value
    cloud_mid_cover: Value
    cloud_high_cover: Value

    # Amount of rain in the past 1h
    precipitation_amount: Value

    # Short wave radiation (light, UV) accumulation
    radiation_short_wave_acc: Value

    # Short wave radiation (light, UV) net accumulation on the surface
    radiation_short_wave_surface_net_acc: Value

    # Long wave radiation (heat, infrared) accumulation
    radiation_long_wave_acc: Value

    # Long wave radiation (light, UV) net accumulation on the surface
    radiation_long_wave_surface_net_acc: Value

    # Diffused short wave
    radiation_short_wave_diff_surface_acc: Value

    geopotential_height: Value
    land_sea_mask: Value


class Weather(NamedTuple):
    """Represents a weather"""
    place: str
    lat: float
    lon: float
    data: WeatherData


class Forecast(NamedTuple):
    """Represents a forecast"""
    place: str
    lat: float
    lon: float
    forecasts: List[WeatherData]
