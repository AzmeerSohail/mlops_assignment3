import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle

# Load the preprocessed data
data = pd.read_csv('processed_data.csv')

# Select features and target
X = data[['humidity_2m', 'wind_speed_10m', 'precipitation']]  # Features
y = data['temperature_2m']  # Target (temperature)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
