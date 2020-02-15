import math
import sys
from datetime import datetime, timezone
from typing import Dict, Any, List
from typing import Optional

import xmltodict

from fmi_weather_client import errors, utils
from fmi_weather_client.models import FMIStation, FMIObservation, FMIStationObservation, Weather


def parse_weather_data(body: str,
                       lat: Optional[float] = None,
                       lon: Optional[float] = None) -> Weather:
    """
    Parse weather information from FMI response
    :param body: HTTP response body from FMI
    :param lat: latitude
    :param lon: longitude
    :return: Weather information
    """
    data = _body_to_dict(body)
    all_observations = _get_observations_per_station(data)

    # Weather by place name return only one station data so let's use it as a default because why not
    closest_observation_set = all_observations[0]

    if lat is not None and lon is not None:
        closest_observation_set = _get_closest_station_observations(lat, lon, all_observations)

    # It is possible that name search or closest station provides no data. Throw an error in that case.
    if len(closest_observation_set.observations) == 0:
        raise errors.NoWeatherDataError

    latest_observation = closest_observation_set.observations[-1]

    return Weather(closest_observation_set.station.name,
                   closest_observation_set.station.lat,
                   closest_observation_set.station.lon,
                   latest_observation)


def parse_multi_weather_data(body: str,
                             lat: float,
                             lon: float) -> Weather:
    """
    Parse weather information from FMI response
    :param body: HTTP response body from FMI
    :param lat: latitude
    :param lon: longitude
    :return: Weather information
    """
    data = _body_to_dict(body)
    all_observations = _get_observations_per_station(data)
    sorted_observation_set = _get_observations_sorted_by_distance(lat, lon, all_observations)

    closest_station = sorted_observation_set[0].station
    latest_observation = sorted_observation_set[0].observations[-1].timestamp

    observations = FMIObservation(latest_observation, lat, lon)
    for station_observation in sorted_observation_set:
        if len(station_observation.observations) > 0:
            latest_variables = station_observation.observations[-1].variables
            for variable_name, value in latest_variables.items():
                if observations.variables.get(variable_name, None) is None and value is not None:
                    observations.variables[variable_name] = value

    return Weather(closest_station.name,
                   closest_station.lat,
                   closest_station.lon,
                   observations)


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
            raise errors.NoWeatherDataError
        raise errors.ServiceError(data['ExceptionReport']['Exception']['ExceptionText'][0])

    if 'wfs:member' not in data['wfs:FeatureCollection'].keys():
        raise errors.NoWeatherDataError

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
                          float(position[0]),
                          float(position[1]))

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


def _get_observation_types(data: Dict[str, Any]) -> List[str]:
    """
    Try to get available observation types (temperature, pressure etc) from the response.
    Available types depends on the available stations.
    :param data: Response data from FMI as xmltodict object
    :return: List of observation types
    """
    observation_types = []
    observation_types_data = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:result']
                              ['gmlcov:MultiPointCoverage']['gmlcov:rangeType']['swe:DataRecord']['swe:field'])
    for observation_type in observation_types_data:
        observation_types.append(observation_type['@name'])
    return observation_types


def _get_observations(data: Dict[str, Any]) -> List[FMIObservation]:
    observation_types = _get_observation_types(data)

    # Get observation times and values for matching. They are different elements in XML but the amount of
    # data points should be the same so times and values can be matched.
    #
    # Time data format is always the same and fields are separated by space:
    # station_longitude station_latitude unix_timestamp
    #
    # Values are also separated by space but number of fields depends on the different variables stations provide.
    # The number of fields should be the same as number of available observation types so these two can be matched.
    #
    observation_times_list = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:result']
                              ['gmlcov:MultiPointCoverage']['gml:domainSet']['gmlcov:SimpleMultiPoint']
                              ['gmlcov:positions'].split('\n'))
    observation_values_list = (data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:result']
                               ['gmlcov:MultiPointCoverage']['gml:rangeSet']['gml:DataBlock']
                               ['gml:doubleOrNilReasonTupleList'].split('\n'))

    observations = []
    for idx, observation_time_data in enumerate(observation_times_list):
        observation_value_data = observation_values_list[idx]
        time_parts = observation_time_data.strip().split(' ')

        # Observation time data. Values are added next.
        observation = FMIObservation(
            datetime.utcfromtimestamp(int(time_parts[3])).replace(tzinfo=timezone.utc),
            float(time_parts[0]),
            float(time_parts[1])
        )

        # Observation variables (temperature, pressure etc..)
        for value_idx, value in enumerate(observation_value_data.strip().split(' ')):
            observation.variables[observation_types[value_idx]] = utils.float_or_none(value)

        # Sometimes the latest observation contains just NaN values. Ignore those.
        if utils.is_non_empty_observation(observation):
            observations.append(observation)

    return observations


def _get_observations_per_station(data: Dict[str, Any]) -> List[FMIStationObservation]:
    """
    This is where the magic happens. It gets all the necessary information from the FMI response combines it
    into one array of dictionaries
    :param data: Response data from FMI as xmltodict object
    :return: List of available observations from one or more weather stations
    """
    output = []

    stations = _get_stations(data)
    observations = _get_observations(data)

    # Observations are matched with stations using coordinates. [wtf.gif]
    # Since observations are ordered by coordinates, let's match them in a simple for-loop instead of trying
    # to do a pointless optimization with dictionaries ;)
    for station in stations:
        station_observations = []
        for observation in observations:
            if station.lat == observation.lat and station.lon == observation.lon:
                station_observations.append(observation)

        output.append(FMIStationObservation(station, station_observations))

    return output


def _get_closest_station_observations(lat: float,
                                      lon: float,
                                      s_observations: List[FMIStationObservation]) -> Optional[FMIStationObservation]:
    """
    Get observations from the closest station
    :param lat: Latitude
    :param lon: Longitude
    :param s_observations: Observations from all stations
    :return: Observations from the closest weather station
    """
    min_distance = sys.maxsize
    closest = None
    for station_observation in s_observations:
        station = station_observation.station
        distance = math.sqrt(((lat - float(station.lat)) ** 2) + ((lon - float(station.lon)) ** 2))
        if distance < min_distance:
            closest = station_observation
            min_distance = distance
    return closest


def _get_observations_sorted_by_distance(lat: float,
                                         lon: float,
                                         s_observations: List[FMIStationObservation]) -> List[FMIStationObservation]:
    """
    Sort observations by distance (closest first)
    :param lat: latitude
    :param lon: longitude
    :param s_observations: Observations
    :return: Observations
    """
    return sorted(s_observations,
                  key=lambda o: math.sqrt(((lat - float(o.station.lat)) ** 2) + ((lon - float(o.station.lon)) ** 2)),
                  reverse=False)
