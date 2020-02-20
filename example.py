import fmi_weather_client
from fmi_weather_client.models import Forecast, Weather, WeatherData


def print_weather(observation: Weather):
    print(observation.place)
    print("Location: %s, %s" % (observation.lat, observation.lon))
    print_weather_data(observation.data)
    print(" ")


def print_forecast(station_forecast: Forecast):
    print("Place: %s" % station_forecast.place)
    print("Location: %s, %s" % (station_forecast.lat, station_forecast.lon))
    for weather in station_forecast.forecasts:
        print_weather_data(weather)
        print("  ")


def print_weather_data(weather: WeatherData):
    print("  Timestamp: %s" % weather.time)
    print("  Temperature: %s" % weather.temperature)
    print("  Humidity: %s" % weather.humidity)
    print("  Wind speed: %s" % weather.wind_speed)
    print("  Cloud cover: %s" % weather.cloud_cover)


weather1 = fmi_weather_client.weather_by_coordinates(60.170998, 24.941325)
weather2 = fmi_weather_client.weather_by_place_name("Kuopio")
forecast1 = fmi_weather_client.forecast_by_place_name("Jäppilä, Pieksämäki")
forecast2 = fmi_weather_client.forecast_by_coordinates(67.6894, 28.62406, timestep_hours=12)

print_weather(weather1)
print_weather(weather2)
print_forecast(forecast1)
print_forecast(forecast2)
