from datetime import datetime
from typing import Optional, List, Dict


class FMIStation:
    def __init__(self, name: str, lat: float, lon: float):
        self.name: str = name
        self.lat: float = lat
        self.lon: float = lon

    def __str__(self):
        return "%s (%s, %s)" % (self.name, self.lat, self.lon)


class FMIForecastTime:
    def __init__(self, lat: float, lon: float, timestamp: datetime):
        self.lat: float = lat
        self.lon: float = lon
        self.timestamp: datetime = timestamp

    def __str__(self):
        return "%s, %s, %s" % (self.lat, self.lon, self.timestamp)


class FMIForecast:
    def __init__(self, lat: float, lon: float, timestamp: datetime, values: Dict[str, float]):
        self.lat: float = lat
        self.lon: float = lon
        self.timestamp: datetime = timestamp
        self.values: Dict[str, float] = values


class Value:
    def __init__(self, value: Optional[float], unit: str):
        self.value: Optional[float] = value
        self.unit: str = unit

    def __str__(self):
        return "%s %s" % (self.value, self.unit)


class WeatherData:
    def __init__(self, timestamp: datetime, values: Dict[str, float]):

        def to_value(o: Dict[str, float], variable_name: str, unit: str) -> Value:
            value = o.get(variable_name, None)
            return Value(value, unit)

        self.time: datetime = timestamp
        self.geopotential_height: Value = to_value(values, 'GeopHeight', 'm')
        self.temperature: Value = to_value(values, 'Temperature', '°C')
        self.pressure: Value = to_value(values, 'Pressure', 'hPa')
        self.humidity: Value = to_value(values, 'Humidity', '%')
        self.wind_direction: Value = to_value(values, 'WindDirection', '°')
        self.wind_speed: Value = to_value(values, 'WindSpeedMS', 'm/s')
        self.wind_u_component: Value = to_value(values, 'WindUMS', 'm/s')
        self.wind_v_component: Value = to_value(values, 'WindVMS', 'm/s')
        self.wind_max: Value = to_value(values, 'MaximumWind', 'm/s')
        self.wind_gust: Value = to_value(values, 'WindGust', 'm/s')
        self.dew_point: Value = to_value(values, 'DewPoint', '°')
        self.cloud_cover: Value = to_value(values, 'TotalCloudCover', '%')
        self.symbol: Value = to_value(values, 'WeatherSymbol3', '')
        self.cloud_low_cover: Value = to_value(values, 'LowCloudCover', '%')
        self.cloud_mid_cover: Value = to_value(values, 'MediumCloudCover', '%')
        self.cloud_high_cover: Value = to_value(values, 'HighCloudCover', '%')
        self.precipitation_amount_1h: Value = to_value(values, 'Precipitation1h', 'mm/h')
        self.precipitation_amount: Value = to_value(values, 'PrecipitationAmount', 'mm')
        self.radiation_global_short_wave_acc: Value = to_value(values, 'RadiationGlobalAccumulation', 'J/m²')
        self.radiation_global_long_wave_acc: Value = to_value(values, 'RadiationLWAccumulation', 'J/m²')
        self.radiation_surface_long_wave_acc: Value = to_value(values, 'RadiationNetSurfaceLWAccumulation', 'J/m²')
        self.radiation_diff_surface_short_wave_acc: Value = to_value(values, 'RadiationDiffuseAccumulation', 'J/m²')
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
