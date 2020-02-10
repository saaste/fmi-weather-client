from datetime import datetime
from typing import Optional
from fmi_weather_client import utils


class WeatherMeasurement:
    def __init__(self, value: float, unit: str):
        self.value: float = value
        self.unit: str = unit

    def __str__(self):
        return "%s %s" % (self.value, self.unit)


class Weather:
    def __init__(self, station_name: str, station_lat: float, station_lon: float, measurement):

        def conv(value, unit):
            if utils.is_float(value):
                return WeatherMeasurement(float(value), unit)
            return None

        self.station_name: str = station_name
        self.station_lat: float = station_lat
        self.station_lon: float = station_lon
        self.measurement_time: datetime = measurement['timestamp']

        self.temperature: Optional[WeatherMeasurement] = conv(measurement.get('t2m', 'nan'), '°C')
        self.humidity: Optional[WeatherMeasurement] = conv(measurement.get('rh', 'nan'), '%')
        self.wind_speed: Optional[WeatherMeasurement] = conv(measurement.get('ws_10min', 'nan'), 'm/s')
        self.wind_gust: Optional[WeatherMeasurement] = conv(measurement.get('wg_10min', 'nan'), 'm/s')
        self.wind_direction: Optional[WeatherMeasurement] = conv(measurement.get('wd_10min', 'nan'), '°')
        self.dew_point: Optional[WeatherMeasurement] = conv(measurement.get('td', 'nan'), '°C')
        self.precipitation_amount: Optional[WeatherMeasurement] = conv(measurement.get('r_1h', 'nan'), 'mm')
        self.precipitation_intensity: Optional[WeatherMeasurement] = conv(measurement.get('ri_10min', 'nan'), 'mm/h')
        self.pressure: Optional[WeatherMeasurement] = conv(measurement.get('p_sea', 'nan'), 'hPa')
        self.visibility: Optional[WeatherMeasurement] = conv(measurement.get('vis', 'nan'), 'm')
        self.cloud_coverage: Optional[WeatherMeasurement] = conv(measurement.get('n_man', 'nan'), '1/8')

        # TODO: Support wawa
        # https://helda.helsinki.fi/bitstream/handle/10138/37284/PRO_GRADU_BOOK_HERMAN.pdf?sequence=2
