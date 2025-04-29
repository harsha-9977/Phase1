# src/utils.py

import pandas as pd

def load_crime_data():
    return pd.read_csv(r'data\crime.csv', encoding='latin1')
