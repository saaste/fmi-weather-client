import os


class MockResponse:
    def __init__(self, xml):
        self.text = xml


def mock_place_response(*args, **kwargs):
    return __mock_response('valid_place_response.xml', args, kwargs)


def mock_bbox_response(*args, **kwargs):
    return __mock_response('valid_bbox_response.xml', args, kwargs)


def mock_empty_response(*args, **kwargs):
    return __mock_response('empty_response.xml', args, kwargs)


def mock_nan_response(*args, **kwargs):
    return __mock_response('nan_response.xml', args, kwargs)


def mock_no_location_exception_response(*args, **kwargs):
    return __mock_response('exception_no_locations_response.xml', args, kwargs)


def mock_other_exception_response(*args, **kwargs):
    return __mock_response('exception_other_response.xml', args, kwargs)


def __mock_response(filename, *args, **kwargs):
    dirname = os.path.dirname(__file__)
    xml_file = os.path.join(dirname, filename)
    with open(xml_file, 'r') as mock_file:
        xml = mock_file.read()

    return MockResponse(xml)
