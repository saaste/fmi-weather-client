from fmi_weather_client import http
from fmi_weather_client.parsers import weather as weather_parser, forecast as forecast_parser
from fmi_weather_client.models import Weather


def weather_by_coordinates(lat: float, lon: float) -> Weather:
    """
    Get the latest weather information by coordinates.

    180 km x 180 km bounding box used to search the closest weather station. Observations are from the past hour.

    :param lat: Latitude (e.g. 25.67087)
    :param lon: Longitude (e.g. 62.39758)
    :return: Latest weather information from the closest weather station
    """
    response = http.request_observations_by_coordinates(lat, lon)
    return weather_parser.parse_weather_data(response, lat, lon)


def weather_by_place_name(name: str) -> Weather:
    """
    Get the latest weather information by place name.

    Search relies of FMI's own service. Observations are from the past hour.

    :param name: Place name (e.g. Kaisaniemi,Helsinki)
    :return: Latest weather information from the closest weather station
    """
    response = http.request_observations_by_place(name)
    return weather_parser.parse_weather_data(response)


def weather_multi_station(lat: float, lon: float) -> Weather:
    """
    Get the latest weather information by combining data from multiple weather stations
    :param lat: Latitude
    :param lon: Longitude
    :return: Latest weather information from multiple weather stations
    """
    response = http.request_observations_by_coordinates(lat, lon)
    return weather_parser.parse_multi_weather_data(response, lat, lon)


def forecast_by_place_name(name: str, timestep_hours: int = 24):
    """
    Get the latest forecast by place name
    :param name: Place name
    :param timestep_hours: Hours between forecasts
    :return: Latest forecast
    """
    response = http.request_forecast_by_place(name, timestep_hours)
    return forecast_parser.parse_forecast(response)


def forecast_by_coordinates(lat: float, lon: float, timestep_hours: int = 24):
    """
    Get the latest forecast by coordinates
    :param lat: Latitude (e.g. 25.67087)
    :param lon: Longitude (e.g. 62.39758)
    :param timestep_hours: Hours between forecasts
    :return: Latest forecast
    """
    response = http.request_forecast_by_coordinates(lat, lon, timestep_hours)
    return forecast_parser.parse_forecast(response)
