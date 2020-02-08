import math
import sys
from datetime import datetime

import fmi_weather.models as models


def try_get_station(station_data):
    name = station_data['gml:Point']['gml:name']
    position = station_data['gml:Point']['gml:pos'].split(' ', 1)
    key = station_data['gml:Point']['gml:pos']
    return {
        key: {
            'name': name,
            'position': {
                'lat': position[0],
                'lon': position[1]
            },
            'measurements': []
        }
    }


def try_get_stations(data):
    stations = {}
    stations_dict = data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:featureOfInterest']['sams:SF_SpatialSamplingFeature']['sams:shape']['gml:MultiPoint']['gml:pointMember']
    if isinstance(stations_dict, list):
        for station_dict in stations_dict:
            station = try_get_station(station_dict)
            stations.update(station)
    else:
        stations.update(try_get_station(stations_dict))
    return stations


def try_get_measurement_value_types(data):
    measurement_types = []
    measurement_types_dicts = data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:result']['gmlcov:MultiPointCoverage']['gmlcov:rangeType']['swe:DataRecord']['swe:field']
    for measurement_type_dict in measurement_types_dicts:
        measurement_types.append(measurement_type_dict['@name'])
    return measurement_types


def try_get_measurement_times(data):
    measurements = []
    measurement_times_dict = data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:result']['gmlcov:MultiPointCoverage']['gml:domainSet']['gmlcov:SimpleMultiPoint']['gmlcov:positions'].split('\n')
    for measurement_dict in measurement_times_dict:
        position_and_time = measurement_dict.strip().split('  ', 1)
        position = position_and_time[0]
        time = datetime.utcfromtimestamp(int(position_and_time[1]))
        measurements.append({
            'position': position,
            'time': time,
            'values': []
        })
    return measurements


def try_get_measurement_value_set(data):
    values = []
    measurement_value_sets = data['wfs:FeatureCollection']['wfs:member']['omso:GridSeriesObservation']['om:result']['gmlcov:MultiPointCoverage']['gml:rangeSet']['gml:DataBlock']['gml:doubleOrNilReasonTupleList'].split('\n')
    for measurement_value_set in measurement_value_sets:
        values.append(measurement_value_set.strip().split(' '))
    return values


def build_data(stations, measurement_types, measurement_times, measurement_value_sets):
    # Combine measurement values with types
    enriched_value_sets = []
    for value_set in measurement_value_sets:
        enriched_value_set = {}
        for value_idx, value in enumerate(value_set):
            enriched_value_set[measurement_types[value_idx]] = value
        enriched_value_sets.append(enriched_value_set)

    # Combine measurement times with enriched values
    enriched_measurement_times = measurement_times.copy()
    for time_idx, time in enumerate(enriched_measurement_times):
        time['values'] = enriched_value_sets[time_idx]

    # Remove measurements with no values
    cleaned_measurement_times = []
    for measurement in enriched_measurement_times:
        for _, value in measurement['values'].items():
            if value != 'NaN':
                cleaned_measurement_times.append(measurement)
                break

    # Combine stations with enriched measurements
    for measurement in cleaned_measurement_times:
        stations[measurement['position']]['measurements'].append(measurement)

    return stations


def get_closest_station(lat, lon, built_data):
    closest_distance = sys.maxsize
    closest_station = None
    for key, station in built_data.items():
        distance = math.sqrt(
            ((lat - float(station['position']['lat'])) ** 2) + ((lon - float(station['position']['lon'])) ** 2))
        if distance < closest_distance:
            closest_station = station
            closest_distance = distance
    return closest_station


def assign_measurements_to_weather(weather, measurements):
    for value_type, value in measurements:
        if value != 'NaN':
            if value_type == 't2m':
                weather.temperature = models.NewWeatherMeasurement(float(value), '°C')
            elif value_type == 'ws_10min':
                weather.wind_speed = models.NewWeatherMeasurement(float(value), 'm/s')
            elif value_type == 'wg_10min':
                weather.wind_gust = models.NewWeatherMeasurement(float(value), 'm/s')
            elif value_type == 'wd_10min':
                weather.wind_direction = models.NewWeatherMeasurement(float(value), '°')
            elif value_type == 'rh':
                weather.humidity = models.NewWeatherMeasurement(float(value), '%')
            elif value_type == 'td':
                weather.dew_point = models.NewWeatherMeasurement(float(value), '°C')
            elif value_type == 'r_1h':
                weather.precipitation_amount = models.NewWeatherMeasurement(float(value), 'mm')
            elif value_type == 'ri_10min':
                weather.precipitation_intensity = models.NewWeatherMeasurement(float(value), 'mm/h')
            elif value_type == 'p_sea':
                weather.pressure = models.NewWeatherMeasurement(float(value), 'hPa')
            elif value_type == 'n_man':
                weather.visibility = models.NewWeatherMeasurement(float(value), '1/8')
            elif value_type == 'wawa':  # TODO: Implement codes: https://helda.helsinki.fi/bitstream/handle/10138/37284/PRO_GRADU_BOOK_HERMAN.pdf?sequence=2
                continue
