from datetime import datetime, timedelta

import requests

from fmi_weather_client import parser

_BASE_URL = 'http://opendata.fmi.fi/wfs'

_DEFAULT_PARAMS = {
    'service': 'WFS',
    'version': '2.0.0',
    'request': 'getFeature',
    'storedquery_id': 'fmi::observations::weather::multipointcoverage',
    'timestep': '10'
}


def weather_by_coordinates(lat: float, lon: float):
    """
    Get the latest weather information by coordinates.

    110 km x 110 km bounding box used to search the closest weather station. Observations are from the past hour.

    :param lat: Latitude (e.g. 25.67087)
    :param lon: Longitude (e.g. 62.39758)
    :return: Latest weather information from the closest weather station
    """
    params = _DEFAULT_PARAMS.copy()
    params.update({
        'bbox': '%s,%s,%s,%s' % (lon - 0.5, lat - 0.5, lon + 0.5, lat + 0.5),
        'starttime': (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
    })

    response = requests.get(_BASE_URL, params=params)
    return parser.parse_weather_data(response, lat, lon)


def weather_by_place_name(name: str):
    """
    Get the latest weather information by place name.

    Search relies of FMI's own service. Observations are from the past hour.

    :param name: Place name (e.g. Kaisaniemi,Helsinki)
    :return: Latest weather information from the closest weather station
    """
    params = _DEFAULT_PARAMS.copy()
    params.update({
        'place': name.strip().replace(' ', ''),
        'starttime': (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
    })

    response = requests.get(_BASE_URL, params=params)
    return parser.parse_weather_data(response)
