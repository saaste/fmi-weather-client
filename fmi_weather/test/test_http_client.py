import unittest
from unittest import mock
from unittest.mock import ANY

import fmi_weather.http_client as http_client


def mocked_requests_get(*args, **kwargs):
    return ''


class FMIHttpClientTest(unittest.TestCase):
    __client = http_client.FMIHttpClient()

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_all_stations(self, mock_get):
        self.__client.get_all_stations()
        expected_params = {'service': 'WFS',
                           'version': '2.0.0',
                           'request': 'getFeature',
                           'storedquery_id': 'fmi::ef::stations',
                           'starttime': ANY}
        mock_get.assert_called_with('http://opendata.fmi.fi/wfs', params=expected_params)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_place_weather(self, mock_get):
        place = 'Helsinki'
        self.__client.get_place_weather(place)
        expected_params = {'service': 'WFS',
                           'version': '2.0.0',
                           'request': 'getFeature',
                           'storedquery_id': 'fmi::observations::weather::timevaluepair',
                           'parameters': 'temperature,windspeedms,rh,td,ri_10min,p_sea,vis,n_man',
                           'timestep': '10',
                           'place': place,
                           'starttime': ANY}
        mock_get.assert_called_with('http://opendata.fmi.fi/wfs', params=expected_params)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_station_weather(self, mock_get):
        station_id = 123456
        self.__client.get_station_weather(station_id)
        expected_params = {'service': 'WFS',
                           'version': '2.0.0',
                           'request': 'getFeature',
                           'storedquery_id': 'fmi::observations::weather::timevaluepair',
                           'parameters': 'temperature,windspeedms,rh,td,ri_10min,p_sea,vis,n_man',
                           'timestep': '10',
                           'fmisid': station_id,
                           'starttime': ANY}
        mock_get.assert_called_with('http://opendata.fmi.fi/wfs', params=expected_params)


if __name__ == '__main__':
    unittest.main()
