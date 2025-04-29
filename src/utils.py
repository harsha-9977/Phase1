# src/utils.py

import pandas as pd

def load_crime_data():
    return pd.read_csv(r'C:\Users\Prajwal\OneDrive\Documents\GitHub\Phase1\data\crime.csv', encoding='latin1')
