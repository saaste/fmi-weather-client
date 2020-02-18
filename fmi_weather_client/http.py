import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests

from fmi_weather_client.errors import ServiceError

_LOGGER = logging.getLogger(__name__)

STORED_QUERY_OBSERVATION = 'fmi::observations::weather::multipointcoverage'
STORED_QUERY_FORECAST = 'fmi::forecast::hirlam::surface::point::multipointcoverage'


def request_observations_by_coordinates(lat: float, lon: float) -> str:
    """
    Get the latest weather information by coordinates.

    180 km x 180 km bounding box used to search the closest weather station. Observations are from the past hour.

    :param lat: Latitude (e.g. 25.67087)
    :param lon: Longitude (e.g. 62.39758)
    :return: Latest weather information from the closest weather station
    """
    params = _create_params(stored_query=STORED_QUERY_OBSERVATION, lat=lat, lon=lon)
    return _send_request(params)


def request_observations_by_place(place: str) -> str:
    """
    Get the latest weather information by place name.

    Search relies of FMI's own service. Observations are from the past hour.

    :param place: Place name (e.g. Kaisaniemi,Helsinki)
    :return: Latest weather information from the closest weather station
    """
    params = _create_params(stored_query=STORED_QUERY_OBSERVATION, place=place)
    return _send_request(params)


def request_forecast_by_coordinates(lat: float, lon: float, timestep_hours: int = 24) -> str:
    """
    Get the latest forecast by place coordinates
    :param lat: Latitude (e.g. 25.67087)
    :param lon: Longitude (e.g. 62.39758)
    :param timestep_hours: Forecast steps in hours
    :return: Forecast response
    """
    params = _create_params(stored_query=STORED_QUERY_FORECAST, timestep_hours=timestep_hours, lat=lat, lon=lon)
    return _send_request(params)


def request_forecast_by_place(place: str, timestep_hours: int = 24) -> str:
    """
    Get the latest forecast by place coordinates
    :param place: Place name (e.g. Kaisaniemi,Helsinki)
    :param timestep_hours: Forecast steps in hours
    :return: Forecast response
    """
    params = _create_params(stored_query=STORED_QUERY_FORECAST, timestep_hours=timestep_hours, place=place)
    return _send_request(params)


def _create_params(stored_query: str,
                   timestep_hours: int = 24,
                   place: Optional[str] = None,
                   lat: Optional[float] = None,
                   lon: Optional[float] = None) -> Dict[str, Any]:
    """
    Create query parameters
    :param stored_query: Name of the stored query. Use STORED_QUERY_* constants
    :param timestep_hours: Timestamp hours (used only by forecast)
    :param place: Place name
    :param lat: Latitude
    :param lon: Longitude
    :return: Parameters
    """

    # Common parameters for all requests
    params = {
        'service': 'WFS',
        'version': '2.0.0',
        'request': 'getFeature',
        'storedquery_id': stored_query,
        'timestep': '10',
    }

    # Set stored query specific parameters
    if stored_query == STORED_QUERY_OBSERVATION:
        params['starttime'] = (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
        params['timestep'] = 10
    elif stored_query == STORED_QUERY_FORECAST:
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        params['starttime'] = now.isoformat(timespec='seconds')
        params['endtime'] = (now + timedelta(days=6)).isoformat(timespec='seconds')
        params['timestamp'] = timestep_hours * 60,
    else:
        raise Exception('Unsupported stored query %s' % stored_query)

    # Set location parameter
    if place is not None:
        params['place'] = place.strip().replace(' ', '')
    elif lat is not None and lon is not None:
        params['bbox'] = '%s,%s,%s,%s' % (lon - 0.8, lat - 0.8, lon + 0.8, lat + 0.8)
    else:
        raise Exception('Location parameter missing')

    return params


def _send_request(params: Dict[str, Any]) -> str:
    """
    Send a request to FMI service and return the body
    :param params: Query parameters
    :return: Response body
    """
    url = 'http://opendata.fmi.fi/wfs'

    _LOGGER.debug("Sending GET to %s with parameters: %s", url, params)
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise ServiceError("Invalid FMI service response", {'status_code': response.status_code, 'body': response.text})

    _LOGGER.debug("Received a response from FMI in %s ms", response.elapsed.microseconds / 1000)
    return response.text
