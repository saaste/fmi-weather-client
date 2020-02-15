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
        self.assertEqual(place_weather.observation_time.timestamp(), 1581331800.0)
        self.assertEqual(place_weather.temperature.value, 3.5)
        self.assertEqual(place_weather.wind_speed.value, 8.9)

    @mock.patch('requests.get', side_effect=test_data.mock_bbox_response)
    def test_get_weather_by_coordinates(self, mock_get):
        place_weather = fmi_weather_client.weather_by_coordinates(63.14343, 27.31317)
        self.assertEqual(place_weather.station_name, 'Kuopio Maaninka')
        self.assertEqual(place_weather.observation_time.timestamp(), 1581331800.0)
        self.assertEqual(place_weather.temperature.value, 2.5)
        self.assertEqual(place_weather.wind_speed.value, 5.3)

    @mock.patch('requests.get', side_effect=test_data.mock_bbox_response)
    def test_get_weather_multi_station(self, mock_get):
        place_weather = fmi_weather_client.weather_multi_station(62.99842, 27.80817)
        self.assertEqual(place_weather.station_name, 'Siilinjärvi Kuopio lentoasema')
        self.assertEqual(place_weather.observation_time.timestamp(), 1581332400.0)
        self.assertEqual(place_weather.temperature.value, 2.0)
        self.assertEqual(place_weather.humidity.value, 91.0)
        self.assertEqual(place_weather.wind_speed.value, 9.9)
        self.assertEqual(place_weather.wind_gust.value, 12.9)
        self.assertEqual(place_weather.wind_direction.value, 174.0)
        self.assertEqual(place_weather.dew_point.value, 0.8)
        self.assertEqual(place_weather.precipitation_amount, None)
        self.assertEqual(place_weather.precipitation_intensity.value, 0.0)
        self.assertEqual(place_weather.pressure.value, 963.2)
        self.assertEqual(place_weather.visibility.value, 19967.0)
        self.assertEqual(place_weather.cloud_coverage.value, 8.0)
        self.assertEqual(place_weather.snow_depth.value, 16.0)
        self.assertEqual(place_weather.wawa.value, 81.0)

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
