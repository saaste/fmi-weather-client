from datetime import datetime, timezone
from typing import Dict, Any, List

import xmltodict

from fmi_weather_client import errors, utils
from fmi_weather_client.models import FMIStation, FMIForecastTime, FMIForecast, Forecast, ForecastItem


def parse_forecast(body: str):
    """
    Parse FMI forecast response body to dictionary and check errors
    :param body: Forecast response body
    :return: Response body as dictionary
    """
    data = _body_to_dict(body)
    stations = _get_stations(data)
    times = _get_forecast_times(data)
    types = _get_forecast_variable_types(data)
    value_sets = _get_forecast_variable_values(data)

    # Combine values with types
    typed_value_sets: List[Dict[str, float]] = []
    for value_set in value_sets:
        typed_value_set = {}
        for idx, value in enumerate(value_set):
            typed_value_set[types[idx]] = value
        typed_value_sets.append(typed_value_set)

    # Combine typed values with times
    forecasts: List[FMIForecast] = []
    for idx, time in enumerate(times):
        forecasts.append(FMIForecast(time.lat, time.lon, time.timestamp, typed_value_sets[idx]))

    # Build forecast objects
    station_forecasts = []
    for station in stations:
        station_forecast = Forecast(station.name, station.lat, station.lon, [])
        for forecast in forecasts:
            if forecast.lat == station.lat and forecast.lon == station.lon and utils.is_non_empty_forecast(
                    forecast.values):
                station_forecast.forecasts.append(ForecastItem(forecast.timestamp, forecast.values))
        station_forecasts.append(station_forecast)

    # I always saw just one station so I guess this is fine
    return station_forecasts[0]


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
            raise errors.NoForecastDataError
        raise errors.ServiceError(data['ExceptionReport']['Exception']['ExceptionText'][0])

    if 'wfs:member' not in data['wfs:FeatureCollection'].keys():
        raise errors.NoForecastDataError

    return data


def _get_stations(data: Dict[str, Any]) -> List[FMIStation]:
    """
    Try to get station data from the response. When call is made with place name, there is only one
    station available. For coordinate search there might be more.
    :param data: Response data from FMI as xmltodict object
    :return: List of stations
    """

    def parse_station_data(station_data: Dict[str, Any]) -> FMIStation:
        name = station_data['gml:Point']['gml:name']
        position = station_data['gml:Point']['gml:pos'].split(' ', 1)
        return FMIStation(name,
                          float(position[1]),
                          float(position[0]))

    stations = []
    stations_dict = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']
                         ['om:featureOfInterest']['sams:SF_SpatialSamplingFeature']['sams:shape']
                         ['gml:MultiPoint']['gml:pointMembers'])

    # xmltodict can return a list or an object depending on how many child the element has
    if isinstance(stations_dict, list):
        for station_dict in stations_dict:
            station = parse_station_data(station_dict)
            stations.append(station)
    else:
        stations.append(parse_station_data(stations_dict))

    return stations


def _get_forecast_times(data: Dict[str, Any]) -> List[FMIForecastTime]:
    result = []
    forecast_times_data_list = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']
                                    ['om:result']['gmlcov:MultiPointCoverage']['gml:domainSet']
                                    ['gmlcov:SimpleMultiPoint']['gmlcov:positions'].split('\n'))
    for forecast_time in forecast_times_data_list:
        parts = forecast_time.strip().replace('  ', ' ').split(' ')
        lon = float(parts[0])
        lat = float(parts[1])
        timestamp = datetime.utcfromtimestamp(int(parts[2])).replace(tzinfo=timezone.utc)
        result.append(FMIForecastTime(lat, lon, timestamp))

    return result


def _get_forecast_variable_types(data) -> List[str]:
    result = []
    variable_type_list = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']
                              ['om:result']['gmlcov:MultiPointCoverage']['gmlcov:rangeType']['swe:DataRecord']
                              ['swe:field'])

    for variable_type in variable_type_list:
        result.append(variable_type['@name'])

    return result


def _get_forecast_variable_values(data: Dict[str, Any]) -> List[List[float]]:
    result = []
    forecast_value_sets = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']
                           ['om:result']['gmlcov:MultiPointCoverage']['gml:rangeSet']['gml:DataBlock']
                           ['gml:doubleOrNilReasonTupleList'].split('\n'))

    for forecast_value_set in forecast_value_sets:
        forecast_values = forecast_value_set.strip().split(' ')
        value_set = []
        for value in forecast_values:
            value_set.append(float(value))
        result.append(value_set)

    return result
