import logging
from datetime import datetime, timedelta
from typing import Any, Dict

import requests

from fmi_weather_client import parser
from fmi_weather_client.errors import ServiceError
from fmi_weather_client.models import Weather

_BASE_URL = 'http://opendata.fmi.fi/wfs'

_DEFAULT_PARAMS = {
    'service': 'WFS',
    'version': '2.0.0',
    'request': 'getFeature',
    'storedquery_id': 'fmi::observations::weather::multipointcoverage',
    'timestep': '10'
}

_LOGGER = logging.getLogger(__name__)


def weather_by_coordinates(lat: float, lon: float) -> Weather:
    """
    Get the latest weather information by coordinates.

    180 km x 180 km bounding box used to search the closest weather station. Observations are from the past hour.

    :param lat: Latitude (e.g. 25.67087)
    :param lon: Longitude (e.g. 62.39758)
    :return: Latest weather information from the closest weather station
    """
    params = {
        'bbox': '%s,%s,%s,%s' % (lon - 0.8, lat - 0.8, lon + 0.8, lat + 0.8),
        'starttime': (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
    }
    response = _request_fmi(params)
    return parser.parse_weather_data(response, lat, lon)


def weather_by_place_name(name: str) -> Weather:
    """
    Get the latest weather information by place name.

    Search relies of FMI's own service. Observations are from the past hour.

    :param name: Place name (e.g. Kaisaniemi,Helsinki)
    :return: Latest weather information from the closest weather station
    """
    params = {
        'place': name.strip().replace(' ', ''),
        'starttime': (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
    }
    response = _request_fmi(params)
    return parser.parse_weather_data(response)


def weather_multi_station(lat: float, lon: float) -> Weather:
    """
    Get the latest full weather by combining data from multiple weather stations
    :param lat: Latitude
    :param lon: Longitude
    :return: Latest weather information from multiple weather stations
    """
    params = {
        'bbox': '%s,%s,%s,%s' % (lon - 0.8, lat - 0.8, lon + 0.8, lat + 0.8),
        'starttime': (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
    }
    response = _request_fmi(params)
    return parser.parse_multi_weather_data(response, lat, lon)


def _request_fmi(params: Dict[str, Any]) -> str:
    """
    Send a request to FMI service and return the body
    :param params: Query parameters
    :return: Response body
    """

    final_params = _DEFAULT_PARAMS.copy()
    final_params.update(params)

    _LOGGER.debug("Sending GET to %s with parameters: %s", _BASE_URL, final_params)
    response = requests.get(_BASE_URL, params=final_params)

    if response.status_code != 200:
        raise ServiceError("Invalid FMI service response", {'status_code': response.status_code, 'body': response.text})

    _LOGGER.debug("Received a response from FMI in %s ms", response.elapsed.microseconds / 1000)
    return response.text
