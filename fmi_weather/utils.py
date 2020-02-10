import math
import sys
from datetime import datetime
from typing import Optional

import xmltodict

import fmi_weather.models as models


class NoWeatherDataError(Exception):
    pass


def try_get_stations(data):
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
            'lon': float(position[0]),
            'lat': float(position[1])
        }

    stations = []

    if 'wfs:member' not in data['wfs:FeatureCollection']:
        raise NoWeatherDataError

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


def try_get_available_measurement_types(data):
    """
    Try to get available measurement types (temperature, pressure etc) from the response. Available types depends
    on the matched stations.
    :param data: Response data from FMI as xmltodict object
    :return: List of measurement types
    """
    measurement_types = []
    measurement_types_dicts = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:result']
                               ['gmlcov:MultiPointCoverage']['gmlcov:rangeType']['swe:DataRecord']['swe:field'])
    for measurement_type_dict in measurement_types_dicts:
        measurement_types.append(measurement_type_dict['@name'])
    return measurement_types


def try_get_measurements(data):
    """
    Try to get available measurements and values
    :param data: Response data from FMI as xmltodict object
    :return: List of measurement values
    """
    def contains_valid_values(vals):
        # Temperature is a must have
        if math.isnan(vals['t2m']):
            return False

        for k, v in vals.items():
            if not math.isnan(v):
                return True
        return False

    measurement_types = try_get_available_measurement_types(data)

    if 'wfs:member' not in data['wfs:FeatureCollection']:
        raise NoWeatherDataError

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
            'lon': float(time_parts[0]),
            'lat': float(time_parts[1]),
            'timestamp': datetime.utcfromtimestamp(int(time_parts[3]))
        }

        # Measurement value data
        values = {}
        for value_idx, value in enumerate(measurement_value_data.strip().split(' ')):
            values[measurement_types[value_idx]] = float(value)

        if contains_valid_values(values):
            measurement.update(values)
            measurements.append(measurement)

    return measurements


def try_get_measurements_per_station(data):
    """
    This is where the magic happens. It gets all the necessary information from the FMI response combines it
    into one array of dictionaries
    :param data: Response data from FMI as xmltodict object
    :return: List of available measurements from one or more weather stations
    """
    output = []

    stations = try_get_stations(data)
    measurements = try_get_measurements(data)

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


def get_closest_measurements(lat, lon, measurements):
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

    throw_on_exception_response(data)

    all_measurements = try_get_measurements_per_station(data)
    if len(all_measurements) == 0:
        raise Exception('No weather data available')

    # Weather by place name return only one station data so let's use it as a default because why not
    closest_measurement_data = all_measurements[0]

    if lat is not None and lon is not None:
        closest_measurement_data = get_closest_measurements(lat, lon, all_measurements)

    latest_measurement = closest_measurement_data['measurements'][-1]

    return models.Weather(closest_measurement_data['station']['name'],
                          closest_measurement_data['station']['lat'],
                          closest_measurement_data['station']['lon'],
                          latest_measurement)


def throw_on_exception_response(data):
    """
    Throw an exception if FMI response contains exception element (service always returns 200)
    :param data: Response data from FMI as xmltodict object
    """
    if 'ExceptionReport' in data.keys():
        raise Exception(data['ExceptionReport']['Exception']['ExceptionText'][0])
    

def is_float(v):
    """
    Make sure the value is float and not a NaN
    :param v:
    :return:
    """
    try:
        f = float(v)
        return not math.isnan(f)
    except (ValueError, TypeError):
        return False
