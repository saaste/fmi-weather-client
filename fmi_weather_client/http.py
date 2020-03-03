import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests

from fmi_weather_client.errors import ServiceError

_LOGGER = logging.getLogger(__name__)


def request_weather_by_coordinates(lat: float, lon: float) -> str:
    """
    Get the latest weather information by coordinates.

    :param lat: Latitude (e.g. 25.67087)
    :param lon: Longitude (e.g. 62.39758)
    :return: Latest weather information
    """
    end_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    start_time = end_time - timedelta(minutes=10)
    params = _create_params(start_time, end_time, 10, lat=lat, lon=lon)
    return _send_request(params)


def request_weather_by_place(place: str) -> str:
    """
    Get the latest weather information by place name.

    :param place: Place name (e.g. Kaisaniemi, Helsinki)
    :return: Latest weather information
    """
    end_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    start_time = end_time - timedelta(minutes=10)
    params = _create_params(start_time, end_time, 10, place=place)
    return _send_request(params)


def request_forecast_by_coordinates(lat: float, lon: float, timestep_hours: int = 24) -> str:
    """
    Get the latest forecast by place coordinates

    :param lat: Latitude (e.g. 25.67087)
    :param lon: Longitude (e.g. 62.39758)
    :param timestep_hours: Forecast steps in hours
    :return: Forecast response
    """
    start_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    end_time = start_time + timedelta(days=4)
    timestep = timestep_hours * 60
    params = _create_params(start_time, end_time, timestep, lat=lat, lon=lon)
    return _send_request(params)


def request_forecast_by_place(place: str, timestep_hours: int = 24) -> str:
    """
    Get the latest forecast by place coordinates

    :param place: Place name (e.g. Kaisaniemi,Helsinki)
    :param timestep_hours: Forecast steps in hours
    :return: Forecast response
    """
    start_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    end_time = start_time + timedelta(days=4)
    timestep = timestep_hours * 60
    params = _create_params(start_time, end_time, timestep, place=place)
    return _send_request(params)


def _create_params(start_time: datetime,
                   end_time: datetime,
                   timestep_minutes: int,
                   place: Optional[str] = None,
                   lat: Optional[float] = None,
                   lon: Optional[float] = None) -> Dict[str, Any]:
    """
    Create query parameters
    :param start_time: Start datetime
    :param end_time: End datetime
    :param timestep_minutes: Timestamp minutes
    :param place: Place name
    :param lat: Latitude
    :param lon: Longitude
    :return: Parameters
    """

    if place is None and lat is None and lon is None:
        raise Exception("Missing location parameter")

    params = {
        'service': 'WFS',
        'version': '2.0.0',
        'request': 'getFeature',
        'storedquery_id': 'fmi::forecast::hirlam::surface::point::multipointcoverage',
        'timestep': timestep_minutes,
        'starttime': start_time.isoformat(timespec='seconds'),
        'endtime': end_time.isoformat(timespec='seconds')
    }

    if lat is not None and lon is not None:
        params['latlon'] = f'{lat},{lon}'

    if place is not None:
        params['place'] = place.strip().replace(' ', '')

    return params


def _send_request(params: Dict[str, Any]) -> str:
    """
    Send a request to FMI service and return the body
    :param params: Query parameters
    :return: Response body
    """
    url = 'http://opendata.fmi.fi/wfs'

    _LOGGER.debug(f"Sending GET to {url} with parameters: {params}")
    response = requests.get(url, params=params)

    if response.status_code >= 500:
        raise ServiceError("Invalid FMI service response", {'status_code': response.status_code, 'body': response.text})

    _LOGGER.debug(f"Received a response from FMI in {response.elapsed.microseconds / 1000} ms", )
    return response.text
