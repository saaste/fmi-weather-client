import unittest
import os

import fmi_weather.xml_parser as xml_parser


def mocked_requests_get(*args, **kwargs):
    return ''


class FMIHttpXMLParserTest(unittest.TestCase):
    __client = xml_parser.FMIXMLParser()

    def test_parse_stations(self):
        dirname = os.path.dirname(__file__)
        xml_file = os.path.join(dirname, 'test_data/fmi_stations_valid_response.xml')

        with open(xml_file, 'r') as mock_file:
            xml_response = mock_file.read()
            result = self.__client.parse_stations(xml_response)

        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].id, 100683)
        self.assertEqual(result[0].name, 'Porvoo Kilpilahti satama')
        self.assertEqual(result[0].region, 'Porvoo')
        self.assertEqual(result[0].country, 'Finland')
        self.assertEqual(result[0].lat, 60.303725)
        self.assertEqual(result[0].lon, 25.549164)

    def test_parse_weather(self):
        dirname = os.path.dirname(__file__)
        xml_file = os.path.join(dirname, 'test_data/fmi_weather_valid_response.xml')

        with open(xml_file, 'r') as mock_file:
            xml_response = mock_file.read()
            result = self.__client.parse_weather(xml_response)

        self.assertEqual(result.location.name, 'Helsinki Kaisaniemi')
        self.assertEqual(result.location.lat, 60.17523)
        self.assertEqual(result.location.lon, 24.94459)
        self.assertEqual(result.cloud_coverage.type, 'cloud_coverage')
        self.assertEqual(result.cloud_coverage.value, 8.0)
        self.assertEqual(result.cloud_coverage.time, '2020-01-31T21:00:00Z')
        self.assertEqual(result.visibility.type, 'visibility')
        self.assertEqual(result.visibility.value, 16860.0)
        self.assertEqual(result.visibility.time, '2020-01-31T21:00:00Z')
        self.assertEqual(result.pressure.type, 'pressure')
        self.assertEqual(result.pressure.value, 999.6)
        self.assertEqual(result.pressure.time, '2020-01-31T21:00:00Z')
        self.assertEqual(result.precipitation.type, 'precipitation')
        self.assertEqual(result.precipitation.value, 0.0)
        self.assertEqual(result.precipitation.time, '2020-01-31T21:00:00Z')
        self.assertEqual(result.dew_point.type, 'dew_point')
        self.assertEqual(result.dew_point.value, 0.4)
        self.assertEqual(result.dew_point.time, '2020-01-31T21:00:00Z')
        self.assertEqual(result.humidity.type, 'humidity')
        self.assertEqual(result.humidity.value, 88.0)
        self.assertEqual(result.humidity.time, '2020-01-31T21:00:00Z')
        self.assertEqual(result.wind_speed.type, 'wind_speed')
        self.assertEqual(result.wind_speed.value, 4.6)
        self.assertEqual(result.wind_speed.time, '2020-01-31T21:00:00Z')
        self.assertEqual(result.temperature.type, 'temperature')
        self.assertEqual(result.temperature.value, 2.2)
        self.assertEqual(result.temperature.time, '2020-01-31T21:00:00Z')

    def test_exception_result_handling(self):
        dirname = os.path.dirname(__file__)
        xml_file = os.path.join(dirname, 'test_data/fmi_exception_response.xml')

        with open(xml_file, 'r') as mock_file:
            xml_response = mock_file.read()

        self.assertRaisesRegex(Exception, 'No locations found', self.__client.parse_weather, xml_response)

    def test_invalid_responses(self):
        self.assertRaisesRegex(Exception, 'XML is not a valid', self.__client.parse_stations, '<tag>invalid</tag>')
        self.assertRaisesRegex(Exception, 'XML is not a valid', self.__client.parse_weather, '<tag>invalid</tag>')


if __name__ == '__main__':
    unittest.main()
