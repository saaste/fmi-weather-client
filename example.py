import fmi_weather_client as fmi
from fmi_weather_client.errors import ClientError, ServerError

try:
    # Get current weather in Kilpisjärvi using coordinates
    kilpisjarvi_weather = fmi.weather_by_coordinates(69.0478, 20.7982)

    # Get forecast for Helsinki
    helsinki_forecast = fmi.forecast_by_place_name("Helsinki")

    # Get observation data
    oulu_observation = fmi.observation_by_station_id(101794)

    # Print current temperature
    print()
    print(f"Temperature @ {kilpisjarvi_weather.place}: {kilpisjarvi_weather.data.temperature}")

    print(f"Temperature @ {oulu_observation.place}: {oulu_observation.data.temperature}")

    # Print temperature forecasts
    print()
    print(f"Forecast for {helsinki_forecast.place}")
    for forecast in helsinki_forecast.forecasts:
        print(f"- Temperature at {forecast.time}: {forecast.temperature}")

except ClientError as err:
    # Catch and print client errors (invalid coordinate, unknown place etc)
    print(f"FMI returned a client error {err.status_code}: {err.message}", err)

except ServerError as err:
    # Catch and print server errors
    print(f"FMI returned a server error {err.status_code}: {err.body}", err)
