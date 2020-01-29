import unittest
import os
import fmi_weather
from unittest import mock


def mock_stations_response(*args, **kwargs):
    class MockResponse:
        def __init__(self, xml):
            self.text = xml

    dirname = os.path.dirname(__file__)
    xml_file = os.path.join(dirname, 'test_data/fmi_stations_valid_response.xml')
    with open(xml_file, 'r') as mock_file:
        xml = mock_file.read()

    return MockResponse(xml)


def mock_weather_response(*args, **kwargs):
    class MockResponse:
        def __init__(self, xml):
            self.text = xml

    dirname = os.path.dirname(__file__)
    xml_file = os.path.join(dirname, 'test_data/fmi_weather_valid_response.xml')
    with open(xml_file, 'r') as mock_file:
        xml = mock_file.read()

    return MockResponse(xml)


class FMIWeatherTest(unittest.TestCase):

    @mock.patch('fmi_weather.http_client.FMIHttpClient.get_all_stations', side_effect=mock_stations_response)
    def test_make_request_stations(self, mock_get):
        closest_station = fmi_weather.get_closest_station(59.9, 19.9)
        self.assertEqual(closest_station.id, 100909)
        self.assertEqual(closest_station.name, 'Lemland Nyhamn')
        self.assertEqual(closest_station.lat, 59.959194)
        self.assertEqual(closest_station.lon, 19.953667)

    @mock.patch('fmi_weather.http_client.FMIHttpClient.get_place_weather', side_effect=mock_weather_response)
    def test_get_weather_by_place(self, mock_get):
        place_weather = fmi_weather.get_weather_by_place('Helsinki Kaisaniemi')
        self.assertEqual(place_weather.location.name, 'Helsinki Kaisaniemi')

    @mock.patch('fmi_weather.http_client.FMIHttpClient.get_station_weather', side_effect=mock_weather_response)
    def test_get_weather_by_station(self, mock_get):
        place_weather = fmi_weather.get_weather_by_station(100909)
        self.assertEqual(place_weather.location.name, 'Helsinki Kaisaniemi')


if __name__ == '__main__':
    unittest.main()
