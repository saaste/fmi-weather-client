# pylint: disable=bad-continuation
# Just because I like to align them like this ;)
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import math
import xmltodict

from fmi_weather_client.models import FMIPlace, Forecast, Value, WeatherData

_LOGGER = logging.getLogger(__name__)


def parse_forecast(body: str):
    """
    Parse FMI forecast response body to dictionary and check errors
    :param body: Forecast response body
    :return: Response body as dictionary
    """
    data = xmltodict.parse(body)

    station = _get_place(data)
    _LOGGER.debug("Received place: %s (%d, %d)", station.name, station.lat, station.lon)

    times = _get_datetimes(data)
    _LOGGER.debug("Received time points: %d", len(times))

    types = _get_value_types(data)
    _LOGGER.debug("Received types: %d", len(types))

    value_sets = _get_values(data)
    _LOGGER.debug("Received value sets: %d", len(value_sets))

    # Combine values with types
    typed_value_sets: List[Dict[str, float]] = []
    for value_set in value_sets:
        typed_value_set = {}
        for idx, value in enumerate(value_set):
            typed_value_set[types[idx]] = value
        typed_value_sets.append(typed_value_set)

    # Combine typed values with times
    forecasts = []
    for idx, time in enumerate(times):
        if _is_non_empty_forecast(typed_value_sets[idx]):
            forecasts.append(_create_weather_data(time, typed_value_sets[idx]))

    _LOGGER.debug("Received non-empty value sets: %d", len(forecasts))

    return Forecast(station.name, station.lat, station.lon, forecasts)


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

    for forecast_value_set in value_sets:
        forecast_values = forecast_value_set.strip().split(' ')
        value_set = []
        for value in forecast_values:
            value_set.append(float(value))

        result.append(value_set)

    return result


def _create_weather_data(time, values: Dict[str, float]) -> WeatherData:
    """Create weather data from raw values"""

    def to_value(vals: Dict[str, float], variable_name: str, unit: str) -> Value:
        value = vals.get(variable_name, None)
        return Value(value, unit)

    return WeatherData(
        time=time,
        temperature=to_value(values, 'Temperature', '°C'),
        dew_point=to_value(values, 'DewPoint', '°C'),
        pressure=to_value(values, 'Pressure', 'hPa'),
        humidity=to_value(values, 'Humidity', '%'),
        wind_direction=to_value(values, 'WindDirection', '°'),
        wind_speed=to_value(values, 'WindSpeedMS', 'm/s'),
        wind_u_component=to_value(values, 'WindUMS', 'm/s'),
        wind_v_component=to_value(values, 'WindVMS', 'm/s'),
        wind_max=to_value(values, 'MaximumWind', 'm/s'),
        wind_gust=to_value(values, 'WindGust', 'm/s'),
        symbol=to_value(values, 'WeatherSymbol3', ''),
        cloud_cover=to_value(values, 'TotalCloudCover', '%'),
        cloud_low_cover=to_value(values, 'LowCloudCover', '%'),
        cloud_mid_cover=to_value(values, 'MediumCloudCover', '%'),
        cloud_high_cover=to_value(values, 'HighCloudCover', '%'),
        precipitation_amount=to_value(values, 'Precipitation1h', 'mm/h'),
        radiation_short_wave_acc=to_value(values, 'RadiationGlobalAccumulation', 'J/m²'),
        radiation_short_wave_surface_net_acc=to_value(values, 'RadiationNetSurfaceSWAccumulation', 'J/m²'),
        radiation_long_wave_acc=to_value(values, 'RadiationLWAccumulation', 'J/m²'),
        radiation_long_wave_surface_net_acc=to_value(values, 'RadiationNetSurfaceLWAccumulation', 'J/m²'),
        radiation_short_wave_diff_surface_acc=to_value(values, 'RadiationDiffuseAccumulation', 'J/m²'),
        geopotential_height=to_value(values, 'GeopHeight', 'm'),
        land_sea_mask=to_value(values, 'LandSeaMask', ''))


def _float_or_none(value: Any) -> Optional[float]:
    """
    Get value as float. None if conversion fails.
    :param value: Any value
    :return: Value as float if successful; None otherwise
    """
    try:
        float_value = float(value)
        if not math.isnan(float_value):
            return float_value
        return None
    except (ValueError, TypeError):
        return None


def _is_non_empty_forecast(forecast: Dict[str, float]) -> bool:
    """
    Check if forecast contains proper values
    :param forecast: Forecast dictionary
    :return: True if forecast contains values; False otherwise
    """
    for _, value in forecast.items():
        if not math.isnan(value):
            return True

    return False
