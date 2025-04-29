from pymongo import MongoClient
import pandas as pd

def load_crime_data():
    try:
        client = MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB
        db = client["nowhere"]  # Your database name
        collection = db["crimes"]  # Your collection name

        # Fetch data from MongoDB and convert it into a DataFrame
        data = list(collection.find())
        if not data:
            return None  # Return None if no data is found

        df = pd.DataFrame(data)
        df = df.drop(columns=['_id'], errors='ignore')  # Drop the _id column if present
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None  # Return None if there's any error during the process
