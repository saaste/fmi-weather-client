from datetime import datetime
from typing import Optional, List, Dict


class FMIStation:
    def __init__(self, name: str, lat: float, lon: float):
        self.name = name
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return "%s (%s, %s)" % (self.name, self.lat, self.lon)


class FMIObservation:
    def __init__(self, timestamp: datetime, lat: float, lon: float):
        self.timestamp: datetime = timestamp
        self.lat: float = lat
        self.lon: float = lon
        self.variables: Dict[str, Optional[float]] = {}


class FMIStationObservation:
    def __init__(self, station: FMIStation, observations: List[FMIObservation]):
        self.station = station
        self.observations = observations


class WeatherMeasurement:
    def __init__(self, value: float, unit: str):
        self.value: float = value
        self.unit: str = unit

    def __str__(self):
        return "%s %s" % (self.value, self.unit)


class Weather:
    def __init__(self, station_name: str, station_lat: float, station_lon: float, observation: FMIObservation):

        def try_get_value(o: FMIObservation, variable_name: str, unit: str):
            value = o.variables.get(variable_name, None)
            if value is not None:
                return WeatherMeasurement(value, unit)
            return None

        self.station_name: str = station_name
        self.station_lat: float = station_lat
        self.station_lon: float = station_lon
        self.observation_time: datetime = observation.timestamp

        self.temperature: Optional[WeatherMeasurement] = try_get_value(observation, 't2m', '°C')
        self.humidity: Optional[WeatherMeasurement] = try_get_value(observation, 'rh', '%')
        self.wind_speed: Optional[WeatherMeasurement] = try_get_value(observation, 'ws_10min', 'm/s')
        self.wind_gust: Optional[WeatherMeasurement] = try_get_value(observation, 'wg_10min', 'm/s')
        self.wind_direction: Optional[WeatherMeasurement] = try_get_value(observation, 'wd_10min', '°')
        self.dew_point: Optional[WeatherMeasurement] = try_get_value(observation, 'td', '°C')
        self.precipitation_amount: Optional[WeatherMeasurement] = try_get_value(observation, 'r_1h', 'mm')
        self.precipitation_intensity: Optional[WeatherMeasurement] = try_get_value(observation, 'ri_10min', 'mm/h')
        self.pressure: Optional[WeatherMeasurement] = try_get_value(observation, 'p_sea', 'hPa')
        self.visibility: Optional[WeatherMeasurement] = try_get_value(observation, 'vis', 'm')
        self.cloud_coverage: Optional[WeatherMeasurement] = try_get_value(observation, 'n_man', '1/8')
        self.snow_depth: Optional[WeatherMeasurement] = try_get_value(observation, 'snow_aws', 'cm')
        # Current weather code (In Finnish: https://www.ilmatieteenlaitos.fi/latauspalvelun-pikaohje)
        self.wawa: Optional[WeatherMeasurement] = try_get_value(observation, 'wawa', '')


class FMIForecastTime:
    def __init__(self, lat: float, lon: float, timestamp: datetime):
        self.lat = lat
        self.lon = lon
        self.timestamp = timestamp

    def __str__(self):
        return "%s, %s, %s" % (self.lat, self.lon, self.timestamp)


class FMIForecast:
    def __init__(self, lat: float, lon: float, timestamp: datetime, values: Dict[str, float]):
        self.lat = lat
        self.lon = lon
        self.timestamp = timestamp
        self.values = values


class ForecastValue:
    def __init__(self, value: float, unit: str):
        self.value = value
        self.unit = unit

    def __str__(self):
        return "%s %s" % (self.value, self.unit)


class ForecastItem:
    def __init__(self, timestamp: datetime, values: Dict[str, float]):

        def try_get_value(o: Dict[str, float], variable_name: str, unit: str) -> Optional[ForecastValue]:
            value = o.get(variable_name, None)
            if value is not None:
                return ForecastValue(value, unit)
            return None

        self.timestamp = timestamp
        self.geopotential_height = try_get_value(values, 'GeopHeight', 'm')
        self.temperature = try_get_value(values, 'Temperature', '°C')
        self.pressure = try_get_value(values, 'Pressure', 'hPa')
        self.humidity = try_get_value(values, 'Humidity', '%')
        self.wind_direction = try_get_value(values, 'WindDirection', '°')
        self.wind_speed = try_get_value(values, 'WindSpeedMS', 'm/s')
        self.wind_u_component = try_get_value(values, 'WindUMS', 'm/s')
        self.wind_v_component = try_get_value(values, 'WindVMS', 'm/s')
        self.wind_max = try_get_value(values, 'MaximumWind', 'm/s')
        self.wind_gust = try_get_value(values, 'WindGust', 'm/s')
        self.dew_point = try_get_value(values, 'DewPoint', '°')
        self.cloud_cover = try_get_value(values, 'TotalCloudCover', '%')
        self.symbol = try_get_value(values, 'WeatherSymbol3', '')
        self.cloud_low_cover = try_get_value(values, 'LowCloudCover', '%')
        self.cloud_mid_cover = try_get_value(values, 'MediumCloudCover', '%')
        self.cloud_high_cover = try_get_value(values, 'HighCloudCover', '%')
        self.precipitation_amount_1h = try_get_value(values, 'Precipitation1h', 'mm/h')
        self.precipitation_amount = try_get_value(values, 'PrecipitationAmount', 'mm')
        self.radiation_global_short_wave_acc = try_get_value(values, 'RadiationGlobalAccumulation', 'J/m²')
        self.radiation_global_long_wave_acc = try_get_value(values, 'RadiationLWAccumulation', 'J/m²')
        self.radiation_surface_long_wave_acc = try_get_value(values, 'RadiationNetSurfaceLWAccumulation', 'J/m²')
        self.radiation_diff_surface_short_wave_acc = try_get_value(values, 'RadiationDiffuseAccumulation', 'J/m²')
        self.land_sea_mask = try_get_value(values, 'LandSeaMask', '')


class Forecast:
    def __init__(self, place: str, lat: float, lon: float, forecasts: List[ForecastItem]):
        self.place = place
        self.lat = lat
        self.lon = lon
        self.forecasts = forecasts
