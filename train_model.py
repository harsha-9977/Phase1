# train_model.py

import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Ensure model directory exists
os.makedirs("models", exist_ok=True)

# Load and prepare data
df = pd.read_csv("data/crime.csv", encoding='latin1')  # or try 'ISO-8859-1'

# Select relevant columns and drop missing values
df = df[["DISTRICT", "DAY_OF_WEEK", "HOUR", "OFFENSE_CODE_GROUP"]].dropna()

# Encode categorical features
X = pd.get_dummies(df[["DISTRICT", "DAY_OF_WEEK", "HOUR"]])
y = df["OFFENSE_CODE_GROUP"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model to disk
joblib.dump(model, "models/crime_model.pkl")

print("✅ Model trained and saved to models/crime_model.pkl")
