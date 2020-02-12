import fmi_weather_client


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


weather = fmi_weather_client.weather_by_coordinates(60.170998, 24.941325)
weather2 = fmi_weather_client.weather_by_place_name("Kuopio")

print_weather(weather)
print('')
print_weather(weather2)
