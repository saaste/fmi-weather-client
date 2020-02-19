import fmi_weather_client
from fmi_weather_client.models import Forecast


def print_weather(weather):
    print(weather.station_name)
    print(weather.observation_time)
    print('Temperature: %s' % weather.temperature)
    print('Dew point: %s' % weather.dew_point)
    print('Humidity: %s' % weather.humidity)
    print('Wind speed: %s' % weather.wind_speed)
    print('Wind gusts: %s' % weather.wind_gust)
    print('Wind direction: %s' % weather.wind_direction)
    print('Precipitation intensity: %s' % weather.precipitation_intensity)
    print('Precipitation amount: %s' % weather.precipitation_amount)
    print('Pressure: %s' % weather.pressure)
    print('Visibility: %s' % weather.visibility)
    print('Cloud coverage: %s' % weather.cloud_coverage)
    print('Snow depth: %s' % weather.snow_depth)
    print('WaWa code: %s', weather.wawa)
    print('')


def print_forecast(station_forecast: Forecast):
    print("Place: %s" % station_forecast.place)
    print("Location: %s, %s" % (station_forecast.lat, station_forecast.lon))

    for forecast in station_forecast.forecasts:
        print("  Timestamp: %s" % forecast.timestamp)
        print("  Temperature: %s" % forecast.temperature)
        print("  Pressure: %s" % forecast.pressure)
        print("  Humidity: %s" % forecast.humidity)
        print("  Wind speed: %s" % forecast.wind_speed)
        print("  Symbol: %", forecast.symbol)
        print("  Cloud cover: %s" % forecast.cloud_cover)
        print("  Low cloud cover: %s" % forecast.cloud_low_cover)
        print("  Mid cloud cover: %s" % forecast.cloud_mid_cover)
        print("  High cloud cover: %s" % forecast.cloud_high_cover)
        print("  Precipitation amount 1h: %s" % forecast.precipitation_amount_1h)
        print("  Precipitation amount: %s" % forecast.precipitation_amount)
        print("  ")


weather = fmi_weather_client.weather_by_coordinates(60.170998, 24.941325)
weather2 = fmi_weather_client.weather_by_place_name("Kuopio")
weather3 = fmi_weather_client.weather_multi_station(69.016989, 21.465569)
forecast = fmi_weather_client.forecast_by_place_name("Jäppilä, Pieksämäki")
forecast2 = fmi_weather_client.forecast_by_coordinates(67.6894, 28.62406, timestep_hours=12)

print_weather(weather)
print_weather(weather2)
print_weather(weather3)
print_forecast(forecast)
print_forecast(forecast2)
