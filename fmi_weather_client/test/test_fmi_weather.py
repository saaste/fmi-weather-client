import unittest
from unittest import mock

import fmi_weather_client
import fmi_weather_client.test.test_data as test_data
from fmi_weather_client.errors import NoDataAvailableError, ServiceError


class FMIWeatherTest(unittest.TestCase):

    @mock.patch('requests.get', side_effect=test_data.mock_place_forecast_response)
    def test_get_observation_by_place(self, mock_get):
        observation = fmi_weather_client.weather_by_place_name('Iisalmi')
        self.assertEqual(observation.place, 'Iisalmi')
        self.assertEqual(observation.data.time.timestamp(), 1582027200.0)
        self.assertEqual(observation.data.temperature.value, 2.34)
        self.assertEqual(observation.data.wind_speed.value, 3.52)

    @mock.patch('requests.get', side_effect=test_data.mock_coordinate_forecast_response)
    def test_get_observation_by_coordinates(self, mock_get):
        observation = fmi_weather_client.weather_by_coordinates(63.14343, 27.31317)
        self.assertEqual(observation.place, 'Sauoiva')
        self.assertEqual(observation.data.time.timestamp(), 1582027200.0)
        self.assertEqual(observation.data.temperature.value, 0.37)
        self.assertEqual(observation.data.wind_speed.value, 1.35)

    @mock.patch('requests.get', side_effect=test_data.mock_empty_response)
    def test_empty_response(self, mock_get):
        with self.assertRaises(NoDataAvailableError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    @mock.patch('requests.get', side_effect=test_data.mock_nan_response)
    def test_nan_response(self, mock_get):
        with self.assertRaises(NoDataAvailableError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    @mock.patch('requests.get', side_effect=test_data.mock_no_location_exception_response)
    def test_no_location_exception_response(self, mock_get):
        with self.assertRaises(NoDataAvailableError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    @mock.patch('requests.get', side_effect=test_data.mock_other_exception_response)
    def test_other_exception_response(self, mock_get):
        with self.assertRaises(ServiceError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    @mock.patch('requests.get', side_effect=test_data.mock_place_forecast_response)
    def test_get_forecast_by_place_name(self, mock_get):
        forecast = fmi_weather_client.forecast_by_place_name('Iisalmi')
        self.assertEqual(forecast.place, 'Iisalmi')
        self.assertEqual(forecast.lat, 27.19067)
        self.assertEqual(forecast.lon, 63.55915)
        self.assertEqual(len(forecast.forecasts), 5)
        self.assertEqual(forecast.forecasts[0].temperature.value, 1.21)
        self.assertEqual(forecast.forecasts[1].pressure.value, 974.67)
        self.assertEqual(forecast.forecasts[4].humidity.value, 96.31)

    @mock.patch('requests.get', side_effect=test_data.mock_coordinate_forecast_response)
    def test_get_forecast_by_coordinates(self, mock_get):
        forecast = fmi_weather_client.forecast_by_coordinates(29.742731, 67.583988)
        self.assertEqual(forecast.place, 'Sauoiva')
        self.assertEqual(forecast.lat, 29.74273)
        self.assertEqual(forecast.lon, 67.58399)
        self.assertEqual(len(forecast.forecasts), 5)
        self.assertEqual(forecast.forecasts[0].temperature.value, -2.26)
        self.assertEqual(forecast.forecasts[1].pressure.value, 968.58)
        self.assertEqual(forecast.forecasts[4].humidity.value, 97.0)


if __name__ == '__main__':
    unittest.main()
