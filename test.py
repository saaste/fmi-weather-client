from fmi_weather.new_version import FMI

weather_client = FMI()
weather = weather_client.weather_by_coordinates(63.361604, 27.392607)
weather2 = weather_client.weather_by_place_name("Mäkkylä, Espoo")
print(weather.location.name)
print('Temperature: %s %s' % (weather.temperature.value, weather.temperature.unit))
print('')
print(weather2.location.name)
print('Temperature: %s %s' % (weather2.temperature.value, weather2.temperature.unit))
print('')
