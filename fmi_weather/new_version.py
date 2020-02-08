from datetime import datetime, timedelta

import requests
import xmltodict

import fmi_weather.models as models
import fmi_weather.utils as utils

class FMI:
    default_params = {
        'service': 'WFS',
        'version': '2.0.0',
        'request': 'getFeature',
    }

    def weather_by_coordinates(self, lat: float, lon: float):
        bbox = '%s,%s,%s,%s' % (lon - 0.9, lat - 0.5, lon + 0.9, lat + 0.5)
        params = FMI.default_params.copy()
        params.update({
            'storedquery_id': 'fmi::observations::weather::multipointcoverage',
            'timestep': '10',
            'bbox': bbox,
            'starttime': (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
        })

        response = requests.get("http://opendata.fmi.fi/wfs", params=params)
        data = xmltodict.parse(response.text)

        # Find measurement stations
        stations = utils.try_get_stations(data)
        measurement_types = utils.try_get_measurement_value_types(data)
        measurement_times = utils.try_get_measurement_times(data)
        measurement_value_sets = utils.try_get_measurement_value_set(data)

        built_data = utils.build_data(stations, measurement_types, measurement_times, measurement_value_sets)
        closest_station = utils.get_closest_station(lat, lon, built_data)
        latest_measurement = closest_station['measurements'][-1]

        weather_location = models.WeatherLocation(closest_station['name'],
                                                  float(closest_station['position']['lat']),
                                                  float(closest_station['position']['lon']))

        weather = models.NewWeather(weather_location, latest_measurement['time'])
        utils.assign_measurements_to_weather(weather, latest_measurement['values'].items())

        return weather


    def weather_by_place_name(self, name: str):
        params = FMI.default_params.copy()
        params.update({
            'storedquery_id': 'fmi::observations::weather::multipointcoverage',
            'timestep': '10',
            'place': name.strip().replace(' ', ''),
            'starttime': (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
        })

        response = requests.get("http://opendata.fmi.fi/wfs", params=params)
        data = xmltodict.parse(response.text)

        # Find measurement stations
        stations = utils.try_get_stations(data)
        measurement_types = utils.try_get_measurement_value_types(data)
        measurement_times = utils.try_get_measurement_times(data)
        measurement_value_sets = utils.try_get_measurement_value_set(data)

        built_data = utils.build_data(stations, measurement_types, measurement_times, measurement_value_sets)
        closest_station = utils.get_closest_station(0.0, 0.0, built_data)
        latest_measurement = closest_station['measurements'][-1]

        weather_location = models.WeatherLocation(closest_station['name'],
                                                  float(closest_station['position']['lat']),
                                                  float(closest_station['position']['lon']))
        weather = models.NewWeather(weather_location, latest_measurement['time'])
        utils.assign_measurements_to_weather(weather, latest_measurement['values'].items())

        return weather
