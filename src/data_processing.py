import pandas as pd

def clean_data(df):
    # Drop missing values
    df.dropna(inplace=True)
    
    # Additional data cleaning steps can be added here
    return df