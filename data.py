import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Define the API URL and parameters for 5-day forecast
url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,relative_humidity_2m,precipitation,rain,wind_speed_10m&hourly=temperature_2m,wind_speed_10m,precipitation,relative_humidity_2m"
params = {
    "latitude": 52.52,  # Example: Berlin
    "longitude": 13.41,
    "hourly": "temperature_2m,wind_speed_10m,precipitation,relative_humidity_2m",  # Data for the next 5 days
    "timezone": "auto",  # Adjust for local timezone
}

try:
    # Fetch the weather data using the Open-Meteo API client
    responses = openmeteo.weather_api(url, params=params)

    # Process the first response (for one location)
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N, {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone: {response.Timezone()} ({response.TimezoneAbbreviation()})")

    # Process hourly forecast data for the next 5 days
    hourly = response.Hourly()
    hourly_data = {
        "date_time": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        ),
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
        "wind_speed_10m": hourly.Variables(2).ValuesAsNumpy(),
        "precipitation": hourly.Variables(3).ValuesAsNumpy(),
    }

    # Convert to a DataFrame
    hourly_dataframe = pd.DataFrame(hourly_data)

    # Display the first few rows of the DataFrame
    print(hourly_dataframe.head())

    # Save to a CSV file
    hourly_dataframe.to_csv("forecast_weather_data.csv", index=False)
    print("Data saved to 'forecast_weather_data.csv'.")

except Exception as e:
    print(f"An error occurred: {e}")
