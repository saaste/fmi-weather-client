import unittest
import fmi_weather_client.http as http
from fmi_weather_client.http import RequestType
from fmi_weather_client.errors import ClientError
from collections import namedtuple


class HTTPTest(unittest.TestCase):

    def test_create_params_missing_location(self):
        with self.assertRaises(Exception):
            http._create_params(RequestType.WEATHER, 10, 4, None, None, None)

    def test_create_params_invalid_request_type(self):
        with self.assertRaises(Exception):
            http._create_params("UNKNOWN", 10, -1, "Test Place", None, None)

    def test_handle_errors_client_error_with_exception_text(self):
        with self.assertRaises(ClientError):
            status_code = 400
            text = """
                <ExceptionReport>
                    <ExceptionText>Mock error</ExceptionText>
                    <ExceptionText>Something else which is not used here </ExceptionText>
                </ExceptionReport>
            """
            Response = namedtuple("Response", ['status_code', 'text'])
            mock_response = Response(status_code=status_code, text=text)
            http._handle_errors(mock_response)
