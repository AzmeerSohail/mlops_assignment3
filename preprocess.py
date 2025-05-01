import pandas as pd
# Preprocess the data
df = pd.read_csv('forecast_weather_data.csv')

# Handling missing values
df.fillna(method='ffill', inplace=True)

# Normalize the data (e.g., temperature and wind speed)
df['temperature_2m'] = (df['temperature_2m'] - df['temperature_2m'].min()) / (df['temperature_2m'].max() - df['temperature_2m'].min())
df['wind_speed_10m'] = (df['wind_speed_10m'] - df['wind_speed_10m'].min()) / (df['wind_speed_10m'].max() - df['wind_speed_10m'].min())

# Save processed data
df.to_csv('processed_data.csv', index=False)
