import unittest
from unittest import mock

import asyncio

import fmi_weather_client
import test.test_data as test_data
from fmi_weather_client.errors import ClientError, ServerError


class FMIWeatherTest(unittest.TestCase):

    # HAPPY CASES
    @mock.patch('requests.get', side_effect=test_data.mock_place_forecast_response)
    def test_get_weather_by_place(self, mock_get):
        weather = fmi_weather_client.weather_by_place_name('Iisalmi')
        self.assert_name_weather(weather)

    @mock.patch('requests.get', side_effect=test_data.mock_place_forecast_response)
    def test_async_get_weather_by_place(self, mock_get):
        loop = asyncio.get_event_loop()
        weather = loop.run_until_complete(fmi_weather_client.async_weather_by_place_name('Iisalmi'))
        self.assert_name_weather(weather)

    @mock.patch('requests.get', side_effect=test_data.mock_coordinate_forecast_response)
    def test_get_weather_by_coordinates(self, mock_get):
        weather = fmi_weather_client.weather_by_coordinates(63.14343, 27.31317)
        self.assert_coordinate_weather(weather)

    @mock.patch('requests.get', side_effect=test_data.mock_coordinate_forecast_response)
    def test_async_get_weather_by_coordinates(self, mock_get):
        loop = asyncio.get_event_loop()
        weather = loop.run_until_complete(fmi_weather_client.async_weather_by_coordinates(63.14343, 27.31317))
        self.assert_coordinate_weather(weather)

    @mock.patch('requests.get', side_effect=test_data.mock_place_forecast_response)
    def test_get_forecast_by_place_name(self, mock_get):
        forecast = fmi_weather_client.forecast_by_place_name('Iisalmi')
        self.assert_name_forecast(forecast)

    @mock.patch('requests.get', side_effect=test_data.mock_place_forecast_response)
    def test_async_get_forecast_by_place_name(self, mock_get):
        loop = asyncio.get_event_loop()
        forecast = loop.run_until_complete(fmi_weather_client.async_forecast_by_place_name('Iisalmi'))
        self.assert_name_forecast(forecast)

    @mock.patch('requests.get', side_effect=test_data.mock_coordinate_forecast_response)
    def test_get_forecast_by_coordinates(self, mock_get):
        forecast = fmi_weather_client.forecast_by_coordinates(29.742731, 67.583988)
        self.assert_coordinate_forecast(forecast)

    @mock.patch('requests.get', side_effect=test_data.mock_coordinate_forecast_response)
    def test_async_get_forecast_by_coordinates(self, mock_get):
        loop = asyncio.get_event_loop()
        forecast = loop.run_until_complete(fmi_weather_client.async_forecast_by_coordinates(67.583988, 29.742731))
        self.assert_coordinate_forecast(forecast)

    # CORNER CASES
    @mock.patch('requests.get', side_effect=test_data.mock_nan_response)
    def test_nil_weather_response(self, mock_get):
        weather_coord = fmi_weather_client.weather_by_coordinates(25.46816, 65.01236)
        weather_name = fmi_weather_client.weather_by_place_name('Oulu')
        self.assertIsNone(weather_coord)
        self.assertIsNone(weather_name)

    @mock.patch('requests.get', side_effect=test_data.mock_nan_response)
    def test_nil_forecast_response(self, mock_get):
        forecast_coord = fmi_weather_client.forecast_by_coordinates(25.46816, 65.01236, 24)
        forecast_name = fmi_weather_client.forecast_by_place_name('Oulu', 24)
        self.assertIsNotNone(forecast_coord)
        self.assertIsNotNone(forecast_name)
        self.assertEqual(forecast_coord.forecasts, [])
        self.assertEqual(forecast_name.forecasts, [])

    # ERROR CASES
    @mock.patch('requests.get', side_effect=test_data.mock_no_location_exception_response)
    def test_no_location_exception_response(self, mock_get):
        with self.assertRaises(ClientError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    @mock.patch('requests.get', side_effect=test_data.mock_invalid_lat_lon_exception_response)
    def test_invalid_lat_lon_exception_response(self, mock_get):
        with self.assertRaises(ClientError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    @mock.patch('requests.get', side_effect=test_data.mock_no_data_available_exception_response)
    def test_no_data_available_exception_response(self, mock_get):
        with self.assertRaises(ClientError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    @mock.patch('requests.get', side_effect=test_data.mock_server_error_response)
    def test_server_error_response(self, mock_get):
        with self.assertRaises(ServerError):
            fmi_weather_client.weather_by_coordinates(27.31317, 63.14343)

    def assert_name_weather(self, weather):
        self.assertEqual(weather.place, 'Iisalmi')
        self.assertEqual(weather.data.time.timestamp(), 1663585800.0)
        self.assertEqual(weather.data.temperature.value, 12.0)
        self.assertEqual(weather.data.dew_point.value, 8.6)
        self.assertEqual(weather.data.pressure.value, 1000.6)
        self.assertEqual(weather.data.humidity.value, 84.9)
        self.assertEqual(weather.data.wind_direction.value, 11.0)
        self.assertEqual(weather.data.wind_speed.value, 4.64)
        self.assertEqual(weather.data.wind_u_component.value, -0.95)
        self.assertEqual(weather.data.wind_v_component.value, -4.54)
        self.assertEqual(weather.data.wind_max.value, None)
        self.assertEqual(weather.data.wind_gust.value, 8.3)
        self.assertEqual(weather.data.symbol.value, 31.0)
        self.assertEqual(weather.data.cloud_cover.value, 98.9)
        self.assertEqual(weather.data.cloud_low_cover.value, 97.3)
        self.assertEqual(weather.data.cloud_mid_cover.value, 79.6)
        self.assertEqual(weather.data.cloud_high_cover.value, 0.0)
        self.assertEqual(weather.data.precipitation_amount.value, 0.1)
        self.assertEqual(weather.data.radiation_short_wave_acc.value, 1095757.4)
        self.assertEqual(weather.data.radiation_short_wave_surface_net_acc.value, 1003347.6)
        self.assertEqual(weather.data.radiation_long_wave_acc.value, None)
        self.assertEqual(weather.data.radiation_long_wave_surface_net_acc.value, -294629.5)
        self.assertEqual(weather.data.radiation_short_wave_diff_surface_acc.value, None)
        self.assertEqual(weather.data.geopotential_height.value, 90.2)
        self.assertEqual(weather.data.land_sea_mask.value, 0.5)

    def assert_coordinate_weather(self, weather):
        self.assertEqual(weather.place, 'Sauoiva')
        self.assertEqual(weather.data.time.timestamp(), 1663585800.0)
        self.assertEqual(weather.data.temperature.value, 6.6)
        self.assertEqual(weather.data.wind_speed.value, 4.79)

    def assert_name_forecast(self, forecast):
        self.assertEqual(forecast.place, 'Iisalmi')
        self.assertEqual(forecast.lat, 63.55915)
        self.assertEqual(forecast.lon, 27.19067)
        self.assertEqual(len(forecast.forecasts), 12)
        self.assertEqual(forecast.forecasts[0].temperature.value, 12.3)
        self.assertEqual(forecast.forecasts[1].pressure.value, 1000.6)
        self.assertEqual(forecast.forecasts[4].humidity.value, 80.7)
        self.assertEqual(forecast.forecasts[5].time.timestamp(), 1663582200)

    def assert_coordinate_forecast(self, forecast):
        self.assertEqual(forecast.place, 'Sauoiva')
        self.assertEqual(forecast.lat, 67.58399)
        self.assertEqual(forecast.lon, 29.74273)
        self.assertEqual(len(forecast.forecasts), 12)
        self.assertEqual(forecast.forecasts[0].temperature.value, 6.8)
        self.assertEqual(forecast.forecasts[1].pressure.value, 1005.8)
        self.assertEqual(forecast.forecasts[4].humidity.value, 97.9)
        self.assertEqual(forecast.forecasts[5].time.timestamp(), 1663582200)


if __name__ == '__main__':
    unittest.main()
