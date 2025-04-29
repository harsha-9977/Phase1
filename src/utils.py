from pymongo import MongoClient
import pandas as pd

def load_crime_data():
    try:

        client = MongoClient('mongodb://localhost:27017/')        
        db = client["nowhere"]
        collection = db["crimes"]

        
        data = list(collection.find())
        if not data:
            return None 

        df = pd.DataFrame(data)
        df = df.drop(columns=['_id'], errors='ignore') 
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None  
