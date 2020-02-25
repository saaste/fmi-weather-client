from datetime import datetime, timezone
from typing import Any, Dict, List

import xmltodict

from fmi_weather_client import errors, utils
from fmi_weather_client.errors import NoDataAvailableError
from fmi_weather_client.models import FMIPlace, Forecast, WeatherData


def parse_forecast(body: str):
    """
    Parse FMI forecast response body to dictionary and check errors
    :param body: Forecast response body
    :return: Response body as dictionary
    """
    data = _body_to_dict(body)
    station = _get_place(data)
    times = _get_datetimes(data)
    types = _get_value_types(data)
    value_sets = _get_values(data)

    # Combine values with types
    typed_value_sets: List[Dict[str, float]] = []
    for value_set in value_sets:
        typed_value_set = {}
        for idx, value in enumerate(value_set):
            typed_value_set[types[idx]] = value
        typed_value_sets.append(typed_value_set)

    # Build forecast objects
    forecast = Forecast(station.name, station.lat, station.lon, [])

    # Combine typed values with times
    for idx, time in enumerate(times):
        if utils.is_non_empty_forecast(typed_value_sets[idx]):
            forecast.forecasts.append(WeatherData(time, typed_value_sets[idx]))

    return forecast


def _body_to_dict(body: str) -> Dict[str, Any]:
    """
    Convert FMI response body to dictionary and check errors
    :param body: FMI response body
    :return: Response as dictionary
    """
    data = xmltodict.parse(body)

    # Check exception response
    if 'ExceptionReport' in data.keys():
        if 'No locations found for the place' in data['ExceptionReport']['Exception']['ExceptionText'][0]:
            raise errors.NoDataAvailableError
        elif 'No data available for' in data['ExceptionReport']['Exception']['ExceptionText'][0]:
            raise errors.NoDataAvailableError
        raise errors.ServiceError(data['ExceptionReport']['Exception']['ExceptionText'][0])

    if 'wfs:member' not in data['wfs:FeatureCollection'].keys():
        raise errors.NoDataAvailableError

    return data


def _get_place(data: Dict[str, Any]) -> FMIPlace:
    place_data = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']
                      ['om:featureOfInterest']['sams:SF_SpatialSamplingFeature']['sams:shape']
                      ['gml:MultiPoint']['gml:pointMembers']['gml:Point'])

    coordinates = place_data['gml:pos'].split(' ', 1)
    lon = float(coordinates[0])
    lat = float(coordinates[1])

    return FMIPlace(place_data['gml:name'], lat, lon)


def _get_datetimes(data: Dict[str, Any]) -> List[datetime]:
    result = []
    forecast_datetimes = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']
                              ['om:result']['gmlcov:MultiPointCoverage']['gml:domainSet']
                              ['gmlcov:SimpleMultiPoint']['gmlcov:positions'].split('\n'))
    for forecast_datetime in forecast_datetimes:
        parts = forecast_datetime.strip().replace('  ', ' ').split(' ')
        timestamp = datetime.utcfromtimestamp(int(parts[2])).replace(tzinfo=timezone.utc)
        result.append(timestamp)

    return result


def _get_value_types(data) -> List[str]:
    result = []
    value_types = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']
                       ['om:result']['gmlcov:MultiPointCoverage']['gmlcov:rangeType']['swe:DataRecord']
                       ['swe:field'])

    for value_type in value_types:
        result.append(value_type['@name'])

    return result


def _get_values(data: Dict[str, Any]) -> List[List[float]]:
    result = []
    value_sets = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']
                      ['om:result']['gmlcov:MultiPointCoverage']['gml:rangeSet']['gml:DataBlock']
                      ['gml:doubleOrNilReasonTupleList'].split('\n'))

    contains_values = False

    for forecast_value_set in value_sets:
        forecast_values = forecast_value_set.strip().split(' ')
        value_set = []
        for value in forecast_values:
            value_set.append(float(value))
            if not contains_values and utils.float_or_none(value) is not None:
                contains_values = True

        result.append(value_set)

    if not contains_values:
        raise NoDataAvailableError

    return result
