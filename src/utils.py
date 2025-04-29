from pymongo import MongoClient
import pandas as pd

def load_crime_data():
    try:

        client = MongoClient("mongodb+srv://root:ananya@cluster0.mongodb.net/nowhere?retryWrites=true&w=majority")
        db = client["nowhere"]
        collection = db["crimes"]

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
