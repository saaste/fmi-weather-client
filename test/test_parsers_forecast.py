import unittest
from fmi_weather_client.parsers.forecast import _float_or_none


class ForecastParserTest(unittest.TestCase):

    def test_float_or_none(self):
        self.assertEqual(_float_or_none("1.0"), 1.0)
        self.assertEqual(_float_or_none("-1.0"), -1.0)
        self.assertEqual(_float_or_none("0.0"), 0.0)
        self.assertEqual(_float_or_none("0"), 0.0)
        self.assertEqual(_float_or_none(""), None)
        self.assertEqual(_float_or_none("NaN"), None)
