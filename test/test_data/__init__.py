import os


class MockElapsed:
    def __init__(self):
        self.microseconds = 10000000


class MockResponse:

    def __init__(self, xml: str, status_code: int):
        self.text: str = xml
        self.status_code: int = status_code
        self.elapsed: MockElapsed = MockElapsed()


def mock_place_forecast_response(*args, **kwargs):
    return __mock_response('valid_place_forecast_response.xml', 200, args, kwargs)


def mock_coordinate_forecast_response(*args, **kwargs):
    return __mock_response('valid_coordinate_forecast_response.xml', 200, args, kwargs)


def mock_nan_response(*args, **kwargs):
    return __mock_response('corner_nan_response.xml', 200, args, kwargs)


def mock_no_location_exception_response(*args, **kwargs):
    return __mock_response('error_no_locations_response.xml', 400, args, kwargs)


def mock_invalid_lat_lon_exception_response(*args, **kwargs):
    return __mock_response('error_invalid_lat_lon_response.xml', 400, args, kwargs)


def mock_no_data_available_exception_response(*args, **kwargs):
    return __mock_response('error_no_data_available_response.xml', 400, args, kwargs)


def mock_server_error_response(*args, **kwargs):
    return MockResponse("Internal Server Error", 500)


def __mock_response(filename, status_code, *args, **kwargs):
    dirname = os.path.dirname(__file__)
    xml_file = os.path.join(dirname, filename)
    with open(xml_file, 'r') as mock_file:
        xml = mock_file.read()

    return MockResponse(xml, status_code)
