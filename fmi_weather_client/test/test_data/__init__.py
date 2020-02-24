import os


class MockElapsed:
    def __init__(self):
        self.microseconds = 10000000


class MockResponse:

    def __init__(self, xml, status_code):
        self.text = xml
        self.status_code = status_code
        self.elapsed = MockElapsed()


def mock_place_forecast_response(*args, **kwargs):
    return __mock_response('valid_place_forecast_response.xml', 200, args, kwargs)


def mock_coordinate_forecast_response(*args, **kwargs):
    return __mock_response('valid_coordinate_forecast_response.xml', 200, args, kwargs)


def mock_empty_response(*args, **kwargs):
    return __mock_response('empty_response.xml', 200, args, kwargs)


def mock_nan_response(*args, **kwargs):
    return __mock_response('nan_response.xml', 200, args, kwargs)


def mock_no_location_exception_response(*args, **kwargs):
    return __mock_response('exception_no_locations_response.xml', 200, args, kwargs)


def mock_other_exception_response(*args, **kwargs):
    return __mock_response('exception_other_response.xml', 200, args, kwargs)


def __mock_response(filename, status_code, *args, **kwargs):
    dirname = os.path.dirname(__file__)
    xml_file = os.path.join(dirname, filename)
    with open(xml_file, 'r') as mock_file:
        xml = mock_file.read()

    return MockResponse(xml, status_code)
