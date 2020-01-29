import requests
from datetime import datetime, timedelta


class FMIHttpClient:
    def __init__(self):
        self.__ns = {
            'ef': 'http://inspire.ec.europa.eu/schemas/ef/4.0',
            'wfs': 'http://www.opengis.net/wfs/2.0',
            'gml': 'http://www.opengis.net/gml/3.2',
            'wml2': 'http://www.opengis.net/waterml/2.0',
            'omso': 'http://inspire.ec.europa.eu/schemas/omso/3.0',
            'om': 'http://www.opengis.net/om/2.0',
            'sams': 'http://www.opengis.net/samplingSpatial/2.0',
            'ows': 'http://www.opengis.net/ows/1.1'
        }

        self.__default_params = {
            'service': 'WFS',
            'version': '2.0.0',
            'request': 'getFeature',
        }

    def get_all_stations(self):
        params = self.__default_params.copy()
        params.update({
            'storedquery_id': 'fmi::ef::stations',
            'starttime': (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
        })
        return requests.get("http://opendata.fmi.fi/wfs", params=params)

    def get_place_weather(self, place: str):
        params = self.__default_params.copy()
        params.update({
            'storedquery_id': 'fmi::observations::weather::timevaluepair',
            'parameters': 'temperature,windspeedms,rh,td,ri_10min,p_sea,vis,n_man',
            'timestep': '10',
            'place': place,
            'starttime': (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
        })
        return requests.get("http://opendata.fmi.fi/wfs", params=params)

    def get_station_weather(self, station_id: int):
        params = self.__default_params.copy()
        params.update({
            'storedquery_id': 'fmi::observations::weather::timevaluepair',
            'parameters': 'temperature,windspeedms,rh,td,ri_10min,p_sea,vis,n_man',
            'timestep': '10',
            'fmisid': station_id,
            'starttime': (datetime.utcnow() + timedelta(hours=-1)).isoformat(timespec='seconds')
        })
        return requests.get("http://opendata.fmi.fi/wfs", params=params)
