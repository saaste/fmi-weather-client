import unittest
from unittest import mock

import fmi_weather_client
import fmi_weather_client.test.test_data as test_data
from fmi_weather_client.errors import NoWeatherDataError, ServiceError


class FMIWeatherTest(unittest.TestCase):

    @mock.patch('requests.get', side_effect=test_data.mock_place_response)
    def test_get_weather_by_place(self, mock_get):
        place_weather = fmi_weather_client.weather_by_place_name('Espoo, Tapiola')
        self.assertEqual(place_weather.station_name, 'Espoo Tapiola')
        self.assertEqual(place_weather.measurement_time.timestamp(), 1581331800.0)
        self.assertEqual(place_weather.temperature.value, 3.5)
        self.assertEqual(place_weather.wind_speed.value, 8.9)

    @mock.patch('requests.get', side_effect=test_data.mock_bbox_response)
    def test_get_weather_by_coordinates(self, mock_get):
        place_weather = fmi_weather_client.weather_by_coordinates(63.14343, 27.31317)
        self.assertEqual(place_weather.station_name, 'Kuopio Maaninka')
        self.assertEqual(place_weather.measurement_time.timestamp(), 1581331800.0)
        self.assertEqual(place_weather.temperature.value, 2.5)
        self.assertEqual(place_weather.wind_speed.value, 5.3)

    @mock.patch('requests.get', side_effect=test_data.mock_empty_response)
    def test_empty_response(self, mock_get):
        with self.assertRaises(NoWeatherDataError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    @mock.patch('requests.get', side_effect=test_data.mock_nan_response)
    def test_nan_response(self, mock_get):
        with self.assertRaises(NoWeatherDataError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    @mock.patch('requests.get', side_effect=test_data.mock_no_location_exception_response)
    def test_no_location_exception_response(self, mock_get):
        with self.assertRaises(NoWeatherDataError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    @mock.patch('requests.get', side_effect=test_data.mock_other_exception_response)
    def test_other_exception_response(self, mock_get):
        with self.assertRaises(ServiceError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)


if __name__ == '__main__':
    unittest.main()
