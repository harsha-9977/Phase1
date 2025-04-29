# src/predictive_model.py

import joblib
import pandas as pd

def load_model():
    return joblib.load("models/crime_model.pkl")

def make_prediction(model, input_data):
    # Prepare input for prediction
    df = pd.DataFrame([input_data])
    df = pd.get_dummies(df)

    # Align columns with training data
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in df.columns:
            df[col] = 0
    df = df[model_features]

    # Make prediction
    prediction = model.predict(df)[0]
    return prediction
