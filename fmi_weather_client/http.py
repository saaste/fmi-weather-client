import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests
import xmltodict

from fmi_weather_client.errors import ClientError, ServerError
from fmi_weather_client.models import RequestType

_LOGGER = logging.getLogger(__name__)


def request_weather_by_coordinates(lat: float, lon: float) -> str:
    """
    Get the latest weather information by coordinates.

    :param lat: Latitude (e.g. 25.67087)
    :param lon: Longitude (e.g. 62.39758)
    :return: Latest weather information
    """
    params = _create_params(RequestType.WEATHER, 10, lat=lat, lon=lon)
    return _send_request(params)


def request_weather_by_place(place: str) -> str:
    """
    Get the latest weather information by place name.

    :param place: Place name (e.g. Kaisaniemi, Helsinki)
    :return: Latest weather information
    """
    params = _create_params(RequestType.WEATHER, 10, place=place)
    return _send_request(params)


def request_forecast_by_coordinates(lat: float, lon: float, timestep_hours: int = 24, forecast_points: int = 4) -> str:
    """
    Get the latest forecast by place coordinates

    :param lat: Latitude (e.g. 25.67087)
    :param lon: Longitude (e.g. 62.39758)
    :param timestep_hours: Forecast steps in hours
    :param forecast_points: number of forcast points
    :return: Forecast response
    """
    timestep_minutes = timestep_hours * 60
    params = _create_params(RequestType.FORECAST, timestep_minutes, forecast_points, lat=lat, lon=lon)
    return _send_request(params)


def request_forecast_by_place(place: str, timestep_hours: int = 24, forecast_points: int = 4) -> str:
    """
    Get the latest forecast by place name

    :param place: Place name (e.g. Kaisaniemi,Helsinki)
    :param timestep_hours: Forecast steps in hours
    :param forecast_points: number of forcast points
    :return: Forecast response
    """
    timestep_minutes = timestep_hours * 60
    params = _create_params(RequestType.FORECAST, timestep_minutes, forecast_points, place=place)
    return _send_request(params)


def request_observation_by_station_id(fmi_sid: int) -> str:
    """
    Get the latest weather information from an observation station.

    :param fmi_sid: Place fmiSID (https://www.ilmatieteenlaitos.fi/havaintoasemat)
    :return: Latest weather information
    """
    params = _create_params(RequestType.OBSERVATION, 10, fmi_sid=fmi_sid)
    return _send_request(params)


def request_observation_by_place(place: str) -> str:
    """
    Get the latest weather information by place name.

    :param place: Place name (e.g. Kaisaniemi, Helsinki)
    :return: Latest weather information
    """
    params = _create_params(RequestType.OBSERVATION, 10, place=place)
    return _send_request(params)


# pylint: disable=too-many-arguments,too-many-positional-arguments
def _create_params(request_type: RequestType,
                   timestep_minutes: int,
                   forecast_points: int = 4,
                   place: Optional[str] = None,
                   fmi_sid: Optional[int] = None,
                   lat: Optional[float] = None,
                   lon: Optional[float] = None) -> Dict[str, Any]:
    """
    Create query parameters
    :param timestep_minutes: Timestamp minutes
    :param forecast_points: number of forcast points
    :param place: Place name
    :param lat: Latitude
    :param lon: Longitude
    :return: Parameters
    """

    if place is None and lat is None and lon is None and fmi_sid is None:
        raise ValueError("Missing location parameter")

    if request_type is RequestType.WEATHER:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=10)
        query_id = "fmi::forecast::edited::weather::scandinavia::point::multipointcoverage"
        parameters = ('Temperature,DewPoint,Pressure,Humidity,WindDirection,WindSpeedMS,'
                      'WindUMS,WindVMS,WindGust,WeatherSymbol3,TotalCloudCover,LowCloudCover,'
                      'MediumCloudCover,HighCloudCover,Precipitation1h,RadiationGlobalAccumulation,'
                      'RadiationNetSurfaceSWAccumulation,RadiationNetSurfaceLWAccumulation,GeopHeight,LandSeaMask')
    elif request_type is RequestType.FORECAST:
        start_time = datetime.now(timezone.utc)
        end_time = start_time + timedelta(minutes=timestep_minutes * forecast_points)
        query_id = "fmi::forecast::edited::weather::scandinavia::point::multipointcoverage"
        parameters = ('Temperature,DewPoint,Pressure,Humidity,WindDirection,WindSpeedMS,'
                      'WindUMS,WindVMS,WindGust,WeatherSymbol3,TotalCloudCover,LowCloudCover,'
                      'MediumCloudCover,HighCloudCover,Precipitation1h,RadiationGlobalAccumulation,'
                      'RadiationNetSurfaceSWAccumulation,RadiationNetSurfaceLWAccumulation,GeopHeight,LandSeaMask')
    elif request_type is RequestType.OBSERVATION:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(minutes=20)
        query_id = "fmi::observations::weather::multipointcoverage"
        parameters = ('Temperature,DewPoint,Pressure,Humidity,WindDirection,WindSpeedMS,'
                      'WindGust,WeatherSymbol3,TotalCloudCover,Precipitation1h')
    else:
        raise ValueError(f"Invalid request_type {request_type}")

    params = {
        'service': 'WFS',
        'version': '2.0.0',
        'request': 'getFeature',
        'storedquery_id': query_id,
        'timestep': timestep_minutes,
        'starttime': start_time.isoformat(timespec='seconds'),
        'endtime': end_time.isoformat(timespec='seconds'),
        'parameters': parameters
    }

    if request_type == RequestType.OBSERVATION and fmi_sid is not None:
        params['fmisid'] = fmi_sid

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
    url = 'https://opendata.fmi.fi/wfs'

    _LOGGER.debug("GET request to %s. Parameters: %s", url, params)
    response = requests.get(url, params=params, timeout=10)

    if response.status_code == 200:
        _validate_response(response)
        _LOGGER.debug("GET response from %s in %d ms. Status: %d.",
                      url,
                      response.elapsed.microseconds / 1000,
                      response.status_code)
    else:
        _handle_errors(response)

    return response.text


def _validate_response(response: requests.Response):
    """Validate response body"""
    data = xmltodict.parse(response.text)

    if ('wfs:FeatureCollection' in data and
            '@numberMatched' in data['wfs:FeatureCollection'] and
            data['wfs:FeatureCollection']['@numberMatched'] == '0'):
        raise ClientError(200, "Valid data source not found with given parameters")


def _handle_errors(response: requests.Response):
    """Handle error responses from FMI service"""
    if 400 <= response.status_code < 500:
        data = xmltodict.parse(response.text)
        try:
            error_message = data['ExceptionReport']['Exception']['ExceptionText'][0]
            raise ClientError(response.status_code, error_message)
        except (KeyError, IndexError) as err:
            raise ClientError(response.status_code, response.text) from err

    raise ServerError(response.status_code, response.text)
