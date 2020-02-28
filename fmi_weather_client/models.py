from datetime import datetime
from typing import Dict, List, Optional


class FMIPlace:
    def __init__(self, name: str, lat: float, lon: float):
        self.name: str = name
        self.lat: float = lat
        self.lon: float = lon

    def __str__(self):
        return f"{self.name} ({self.lat}, {self.lon})"


class Value:
    def __init__(self, value: Optional[float], unit: str):
        self.value: Optional[float] = value
        self.unit: str = unit

    def __str__(self):
        return f"{self.value} {self.unit}"


class WeatherData:
    def __init__(self, timestamp: datetime, values: Dict[str, float]):

        def to_value(o: Dict[str, float], variable_name: str, unit: str) -> Value:
            value = o.get(variable_name, None)
            return Value(value, unit)

        self.time: datetime = timestamp

        self.temperature: Value = to_value(values, 'Temperature', '°C')
        self.dew_point: Value = to_value(values, 'DewPoint', '°C')

        self.pressure: Value = to_value(values, 'Pressure', 'hPa')
        self.humidity: Value = to_value(values, 'Humidity', '%')

        self.wind_direction: Value = to_value(values, 'WindDirection', '°')
        self.wind_speed: Value = to_value(values, 'WindSpeedMS', 'm/s')
        self.wind_u_component: Value = to_value(values, 'WindUMS', 'm/s')
        self.wind_v_component: Value = to_value(values, 'WindVMS', 'm/s')
        self.wind_max: Value = to_value(values, 'MaximumWind', 'm/s')  # Max 10 min average
        self.wind_gust: Value = to_value(values, 'WindGust', 'm/s')  # Max 3 sec average

        self.symbol: Value = to_value(values, 'WeatherSymbol3', '')
        self.cloud_cover: Value = to_value(values, 'TotalCloudCover', '%')

        self.cloud_low_cover: Value = to_value(values, 'LowCloudCover', '%')
        self.cloud_mid_cover: Value = to_value(values, 'MediumCloudCover', '%')
        self.cloud_high_cover: Value = to_value(values, 'HighCloudCover', '%')

        # Amount of rain in the past 1h
        self.precipitation_amount: Value = to_value(values, 'Precipitation1h', 'mm/h')

        # No idea what this is since it is missing the time
        # self.precipitation_amount: Value = to_value(values, 'PrecipitationAmount', 'mm')

        # Short wave radiation (light, UV) accumulation
        self.radiation_short_wave_acc: Value = to_value(values, 'RadiationGlobalAccumulation', 'J/m²')

        # Short wave radiation (light, UV) net accumulation on the surface
        self.radiation_short_wave_surface_net_acc: Value = to_value(values, 'RadiationNetSurfaceSWAccumulation', 'J/m²')

        # Long wave radiation (heat, infrared) accumulation
        self.radiation_long_wave_acc: Value = to_value(values, 'RadiationLWAccumulation', 'J/m²')

        # Long wave radiation (light, UV) net accumulation on the surface
        self.radiation_long_wave_surface_net_acc: Value = to_value(values, 'RadiationNetSurfaceLWAccumulation', 'J/m²')

        # Diffused short wave
        self.radiation_short_wave_diff_surface_acc: Value = to_value(values, 'RadiationDiffuseAccumulation', 'J/m²')

        self.geopotential_height: Value = to_value(values, 'GeopHeight', 'm')
        self.land_sea_mask: Value = to_value(values, 'LandSeaMask', '')


class Weather:
    def __init__(self, place: str, lat: float, lon: float, weather_data: WeatherData):
        self.place: str = place
        self.lat: float = lat
        self.lon: float = lon
        self.data: WeatherData = weather_data


class Forecast:
    def __init__(self, place: str, lat: float, lon: float, forecasts: List[WeatherData]):
        self.place: str = place
        self.lat: float = lat
        self.lon: float = lon
        self.forecasts: List[WeatherData] = forecasts
