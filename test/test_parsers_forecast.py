import unittest
from fmi_weather_client.parsers.forecast import _float_or_none
from fmi_weather_client.parsers.forecast import _feels_like


class ForecastParserTest(unittest.TestCase):

    def test_float_or_none(self):
        self.assertEqual(_float_or_none("1.0"), 1.0)
        self.assertEqual(_float_or_none("-1.0"), -1.0)
        self.assertEqual(_float_or_none("0.0"), 0.0)
        self.assertEqual(_float_or_none("0"), 0.0)
        self.assertEqual(_float_or_none(""), None)
        self.assertEqual(_float_or_none("NaN"), None)

    def test_feels_like(self):
        # Partial data
        self.assertEqual(_feels_like({}), None)
        self.assertEqual(_feels_like({"Temperature": 10}), 10)
        self.assertEqual(_feels_like({"Temperature": 10, "WindSpeedMS": 10}), 10)
        self.assertEqual(_feels_like({"Temperature": 10, "Humidity": 10}), 10)
        # Without radiation
        self.assertAlmostEqual(_feels_like({"WindSpeedMS": 5, "Humidity": 50, "Temperature": 0}), -4.980, places=3)
        self.assertAlmostEqual(_feels_like({"WindSpeedMS": 5, "Humidity": 50, "Temperature": -5}), -10.653, places=3)
        self.assertAlmostEqual(_feels_like({"WindSpeedMS": 5, "Humidity": 50, "Temperature": 25}), 23.385, places=3)
        self.assertAlmostEqual(_feels_like({"WindSpeedMS": 5, "Humidity": 90, "Temperature": 25}), 26.588, places=3)
        # With radiation
        self.assertAlmostEqual(
            _feels_like({"WindSpeedMS": 0, "Humidity": 50, "Temperature": 0, "RadiationGlobal": 0}),
            -0.250, places=3)
        self.assertAlmostEqual(
            _feels_like({"WindSpeedMS": 0, "Humidity": 50, "Temperature": 10, "RadiationGlobal": 50}),
            9.995, places=3)
        self.assertAlmostEqual(
            _feels_like({"WindSpeedMS": 5, "Humidity": 50, "Temperature": 0, "RadiationGlobal": 800}),
            -2.617, places=3)
        self.assertAlmostEqual(
            _feels_like({"WindSpeedMS": 5, "Humidity": 50, "Temperature": 25, "RadiationGlobal": 425}),
            24.523, places=3)
