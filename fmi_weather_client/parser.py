import math
import sys
from datetime import datetime, timezone
from typing import Optional
import xmltodict

from fmi_weather_client import errors, models, utils


def parse_weather_data(response,
                       lat: Optional[float] = None,
                       lon: Optional[float] = None):
    """
    Parse weather information from FMI response
    :param response: HTTP response
    :param lat: latitude
    :param lon: longitude
    :return: Weather information
    """
    data = xmltodict.parse(response.text)

    # Check exception response
    if 'ExceptionReport' in data.keys():
        if 'No locations found for the place' in data['ExceptionReport']['Exception']['ExceptionText'][0]:
            raise errors.NoWeatherDataError
        raise errors.ServiceError(data['ExceptionReport']['Exception']['ExceptionText'][0])

    if 'wfs:member' not in data['wfs:FeatureCollection'].keys():
        raise errors.NoWeatherDataError

    all_measurements = _try_get_measurements_per_station(data)

    # Weather by place name return only one station data so let's use it as a default because why not
    closest_measurement_data = all_measurements[0]

    if lat is not None and lon is not None:
        closest_measurement_data = _get_closest_measurements(lat, lon, all_measurements)

    # It is possible that name search or closest station provides no data. Throw an error in that case.
    if len(closest_measurement_data['measurements']) == 0:
        raise errors.NoWeatherDataError

    latest_measurement = closest_measurement_data['measurements'][-1]

    return models.Weather(closest_measurement_data['station']['name'],
                          closest_measurement_data['station']['lat'],
                          closest_measurement_data['station']['lon'],
                          latest_measurement)


def _try_get_stations(data):
    """
    Try to get station data from the response. When call is made with place name, there is only one
    station available. For coordinate search there might be more.
    :param data: Response data from FMI as xmltodict object
    :return: List of stations
    """

    def parse_station_data(station_data):
        name = station_data['gml:Point']['gml:name']
        position = station_data['gml:Point']['gml:pos'].split(' ', 1)
        return {
            'name': name,
            'lat': float(position[0]),
            'lon': float(position[1])
        }

    stations = []
    stations_dict = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']
                     ['om:featureOfInterest']['sams:SF_SpatialSamplingFeature']['sams:shape']['gml:MultiPoint']
                     ['gml:pointMember'])

    # xmltodict can return a list or an object depending on how many child the element has
    if isinstance(stations_dict, list):
        for station_dict in stations_dict:
            station = parse_station_data(station_dict)
            stations.append(station)
    else:
        stations.append(parse_station_data(stations_dict))

    return stations


def _try_get_observation_types(data):
    """
    Try to get available observation types (temperature, pressure etc) from the response.
    Available types depends on the available stations.
    :param data: Response data from FMI as xmltodict object
    :return: List of measurement types
    """
    measurement_types = []
    measurement_types_dicts = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:result']
                               ['gmlcov:MultiPointCoverage']['gmlcov:rangeType']['swe:DataRecord']['swe:field'])
    for measurement_type_dict in measurement_types_dicts:
        measurement_types.append(measurement_type_dict['@name'])
    return measurement_types


def _try_get_measurements(data):
    measurement_types = _try_get_observation_types(data)

    # Get measurement times and values for matching. They are different elements in XML but the amount of
    # data points should be the same so times and values can be matched.
    #
    # Time data format is always the same and fields are separated by space:
    # station_longitude station_latitude unix_timestamp
    #
    # Values are also separated by space but number of fields depends on the different measurements stations provide.
    # The number of fields should be the same as number of available measurement types so these two can be matched.
    #
    measurement_times_array = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:result']
                               ['gmlcov:MultiPointCoverage']['gml:domainSet']['gmlcov:SimpleMultiPoint']
                               ['gmlcov:positions'].split('\n'))
    measurement_values_arrays = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:result']
                                 ['gmlcov:MultiPointCoverage']['gml:rangeSet']['gml:DataBlock']
                                 ['gml:doubleOrNilReasonTupleList'].split('\n'))

    measurements = []
    for idx, measurement_time_data in enumerate(measurement_times_array):
        measurement_value_data = measurement_values_arrays[idx]
        time_parts = measurement_time_data.strip().split(' ')

        # Measurement time data. Values are added next.
        measurement = {
            'lat': float(time_parts[0]),
            'lon': float(time_parts[1]),
            'timestamp': datetime.utcfromtimestamp(int(time_parts[3])).replace(tzinfo=timezone.utc)
        }

        # Measurement value data
        values = {}
        for value_idx, value in enumerate(measurement_value_data.strip().split(' ')):
            values[measurement_types[value_idx]] = float(value)

        # Sometimes the latest observation contains just NaN values. Ignore those.
        if utils.is_non_empty_observation(values):
            measurement.update(values)
            measurements.append(measurement)

    return measurements


def _try_get_measurements_per_station(data):
    """
    This is where the magic happens. It gets all the necessary information from the FMI response combines it
    into one array of dictionaries
    :param data: Response data from FMI as xmltodict object
    :return: List of available measurements from one or more weather stations
    """
    output = []

    stations = _try_get_stations(data)
    measurements = _try_get_measurements(data)

    # Measurements are matched with stations using coordinates. [wtf.gif]
    # Since measurements are ordered by coordinates, let's match them in a simple for-loop instead of trying
    # to do a pointless optimization with dictionaries ;)
    for station in stations:
        station_measurements = []
        for measurement in measurements:
            if station['lat'] == measurement['lat'] and station['lon'] == measurement['lon']:
                station_measurements.append(measurement)

        output.append({
            'station': station,
            'measurements': station_measurements
        })

    return output


def _get_closest_measurements(lat, lon, measurements):
    """
    Get measurements from the closest station
    :param lat: Latitude
    :param lon: Longitude
    :param measurements: Measurements from all stations
    :return: Measurements from the closes weather station
    """
    closest_distance = sys.maxsize
    closest_measurement = None
    for measurement in measurements:
        station = measurement['station']
        distance = math.sqrt(((lat - float(station['lat'])) ** 2) + ((lon - float(station['lon'])) ** 2))
        if distance < closest_distance:
            closest_measurement = measurement
            closest_distance = distance
    return closest_measurement
