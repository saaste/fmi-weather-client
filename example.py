import fmi_weather

closest_station = fmi_weather.get_closest_station(60.22, 24.83)
weather = fmi_weather.get_weather_by_station(closest_station.id)

print("Station: %s" % weather.location.name)
print("")
print("Temperature: %s °C" % weather.temperature.value if weather.temperature is not None else '-')
print("Wind: %s m/s" % weather.wind_speed.value if weather.wind_speed is not None else '-')
print("Humidity: %s %%" % weather.humidity.value if weather.humidity is not None else '-')
print("Dew point: %s °C" % weather.dew_point.value if weather.dew_point is not None else '-')
print("Precipitation: %s mm/h" % weather.precipitation.value if weather.precipitation is not None else '-')
print("Pressure: %s hPa" % weather.pressure.value if weather.pressure is not None else '-')
print("Visibility: %s m" % weather.visibility.value if weather.visibility is not None else '-')
print("Cloud coverage: %s/8" % (int(weather.cloud_coverage.value) if weather.cloud_coverage is not None else '-'))
