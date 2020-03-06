import unittest
from fmi_weather_client.models import FMIPlace, Value


class ModelsTest(unittest.TestCase):

    def test_fmi_place(self):
        subject = FMIPlace(name="Helsinki", lat=12.3456, lon=98.7654)
        self.assertEqual(f"{subject}", "Helsinki (12.3456, 98.7654)")

    def test_value(self):
        subject = Value(value=-23.12, unit="°C")
        self.assertEqual(f"{subject}", "-23.12 °C")

        subject = Value(value=-23.12, unit="")
        self.assertEqual(f"{subject}", "-23.12")

        subject = Value(value=None, unit="°C")
        self.assertEqual(f"{subject}", "- °C")

        subject = Value(value=None, unit="")
        self.assertEqual(f"{subject}", "-")
