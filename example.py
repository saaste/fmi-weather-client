import fmi_weather


def print_weather(weather):
    print(weather.station_name)
    print(weather.measurement_time)
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


weather = fmi_weather.weather_by_coordinates(67.2463, 23.6659)
weather2 = fmi_weather.weather_by_place_name("Iisalmi")

print_weather(weather)
print('')
print_weather(weather2)
