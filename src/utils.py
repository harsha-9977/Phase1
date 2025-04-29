# src/utils.py

import pandas as pd

def load_crime_data():
    return pd.read_csv(r'C:\Users\shrey\Downloads\another\another\data\crime.csv', encoding='latin1')
