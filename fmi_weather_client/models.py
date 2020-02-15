from datetime import datetime
from typing import Optional, List, Dict


class FMIStation:
    def __init__(self, name: str, lat: float, lon: float):
        self.name = name
        self.lat = lat
        self.lon = lon


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

        # TODO: Support wawa
        # https://helda.helsinki.fi/bitstream/handle/10138/37284/PRO_GRADU_BOOK_HERMAN.pdf?sequence=2
