from xml.etree.ElementTree import fromstring
import math
import fmi_weather.models as models
import typing


class FMIXMLParser:

    def __init__(self):
        self.__ns = {
            'ef': 'http://inspire.ec.europa.eu/schemas/ef/4.0',
            'wfs': 'http://www.opengis.net/wfs/2.0',
            'gml': 'http://www.opengis.net/gml/3.2',
            'wml2': 'http://www.opengis.net/waterml/2.0',
            'omso': 'http://inspire.ec.europa.eu/schemas/omso/3.0',
            'om': 'http://www.opengis.net/om/2.0',
            'sams': 'http://www.opengis.net/samplingSpatial/2.0',
            'ows': 'http://www.opengis.net/ows/1.1'
        }

        self.is_valid = False

    def parse_stations(self, s) -> typing.List[models.Station]:
        stations = []
        root = fromstring(s)

        self.__throw_if_exception(root)
        self.__throw_if_not_stations_result(root)

        members = root.findall("wfs:member", self.__ns)

        for member in members:
            facility = member.find('ef:EnvironmentalMonitoringFacility', self.__ns)
            if not self.__is_automatic_weather_station(facility):
                continue

            station = models.Station(int(facility.find('gml:identifier', self.__ns).text))

            names = facility.findall('gml:name', self.__ns)
            for name in names:
                if name.attrib['codeSpace'] == 'http://xml.fmi.fi/namespace/locationcode/name':
                    station.name = name.text
                elif name.attrib['codeSpace'] == 'http://xml.fmi.fi/namespace/location/region':
                    station.region = name.text
                elif name.attrib['codeSpace'] == 'http://xml.fmi.fi/namespace/location/country':
                    station.country = name.text

            point = facility.find('ef:representativePoint', self.__ns).find('gml:Point', self.__ns)
            pos = point.find('gml:pos', self.__ns).text.split(' ', 1)
            station.lat = float(pos[0])
            station.lon = float(pos[1])
            stations.append(station)

        return stations

    def parse_weather(self, s) -> models.Weather:
        root = fromstring(s)

        self.__throw_if_exception(root)
        self.__throw_if_not_weather_result(root)

        members = root.findall("wfs:member", self.__ns)
        location = self.__find_location(members[0])
        weather = models.Weather(location)

        for member in members:
            measurement = self.__find_measurement(member)
            if measurement is not None:
                setattr(weather, measurement.type, measurement)
        return weather

    def __is_automatic_weather_station(self, facility):
        for belongs_to in facility.findall('ef:belongsTo', self.__ns):
            if belongs_to.attrib['{http://www.w3.org/1999/xlink}title'] == 'Automaattinen sääasema':
                return True
        return False

    def __find_location(self, member):
        observation = member.find("omso:PointTimeSeriesObservation", self.__ns)
        feature_of_interest = observation.find('om:featureOfInterest', self.__ns)
        sampling_feature = feature_of_interest.find('sams:SF_SpatialSamplingFeature', self.__ns)
        shape = sampling_feature.find('sams:shape', self.__ns)
        point = shape.find('gml:Point', self.__ns)
        name = point.find('gml:name', self.__ns).text
        position = point.find('gml:pos', self.__ns).text.strip().split(' ', 1)
        return models.WeatherLocation(name, float(position[0]), float(position[1]))

    def __find_measurement(self, member):

        measurement_type = self.__find_measurement_type(member)
        if measurement_type is None:
            return None

        observation = member.find("omso:PointTimeSeriesObservation", self.__ns)
        result = observation.find('om:result', self.__ns)
        measurement_time_series = result.find('wml2:MeasurementTimeseries', self.__ns)

        points = list(measurement_time_series)
        points.reverse()

        for point in points:
            measurement_tvp = point.find('wml2:MeasurementTVP', self.__ns)
            value = float(measurement_tvp.find('wml2:value', self.__ns).text)

            if not math.isnan(value):
                time = point.find('wml2:MeasurementTVP', self.__ns).find('wml2:time', self.__ns).text
                return models.WeatherMeasurement(measurement_type, time, value)

        return None

    def __find_measurement_type(self, member):
        observation = member.find("omso:PointTimeSeriesObservation", self.__ns)
        result = observation.find('om:result', self.__ns)
        measurement = result.find('wml2:MeasurementTimeseries', self.__ns)
        raw_type = measurement.attrib['{http://www.opengis.net/gml/3.2}id'].replace('obs-obs-1-1-', '')
        switcher = {
            'temperature': 'temperature',
            'rh': 'humidity',
            'windspeedms': 'wind_speed',
            'td': 'dew_point',
            'ri_10min': 'precipitation',
            'p_sea': 'pressure',
            'vis': 'visibility',
            'n_man': 'cloud_coverage'
        }
        return switcher.get(raw_type, None)

    def __throw_if_exception(self, root):
        if root.tag == '{http://www.opengis.net/ows/1.1}ExceptionReport':
            raise Exception(root.find('ows:Exception', self.__ns).find('ows:ExceptionText', self.__ns).text)

    def __throw_if_not_stations_result(self, root):
        exception = Exception('XML is not a valid station list response')
        try:
            member = root.find('wfs:member', self.__ns)
            facility = member.find('ef:EnvironmentalMonitoringFacility', self.__ns)
            if facility is None:
                raise exception
        except Exception:
            raise exception

    def __throw_if_not_weather_result(self, root):
        exception = Exception('XML is not a valid weather response')
        try:
            member = root.find('wfs:member', self.__ns)
            observation = member.find('omso:PointTimeSeriesObservation', self.__ns)
            if observation is None:
                raise exception
        except Exception:
            raise exception
