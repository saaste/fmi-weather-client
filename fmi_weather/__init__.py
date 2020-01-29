from typing import Optional
from fmi_weather.models import Station
import math
import fmi_weather.http_client as fmi_http_client
import fmi_weather.xml_parser as fmi_xml_parser


def get_closest_station(lat: float, lon: float) -> Optional[Station]:
    """
    Get closest weather station

    :param lat: Latitude
    :param lon: Longitude
    :return: Closest weather station if found; None otherwise
    """
    http = fmi_http_client.FMIHttpClient()
    xml = fmi_xml_parser.FMIXMLParser()

    response = http.get_all_stations()
    stations = xml.parse_stations(response.text)

    closest_station = None
    closest_distance = float('inf')

    for station in stations:
        distance = math.sqrt(((lat - station.lat) ** 2) + ((lon - station.lon) ** 2))
        if distance < closest_distance:
            closest_distance = distance
            closest_station = station

    return closest_station


def get_weather_by_place(place: str):
    """
    Get weather report by a place

    :param place: Place name (e.g. "Helsinki" or "Leppävaara, Espoo")
    :return: Weather report
    """
    http = fmi_http_client.FMIHttpClient()
    xml = fmi_xml_parser.FMIXMLParser()
    response = http.get_place_weather(place.replace(" ", ""))
    return xml.parse_weather(response.text)


def get_weather_by_station(station_id: int):
    """
    Get weather report by a station

    :param station_id: Station ID
    :return: Weather report
    """
    http = fmi_http_client.FMIHttpClient()
    xml = fmi_xml_parser.FMIXMLParser()
    response = http.get_station_weather(station_id)
    return xml.parse_weather(response.text)
