from pymongo import MongoClient
import pandas as pd

def fetch_data():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB URI
    db = client['nowhere']  # Replace with your database name
    collection = db['crimes']  # Replace with your collection name

    # Fetch data
    data = list(collection.find())
    df = pd.DataFrame(data)
    
    return df

# if __name__ == "__main__":
#     df = fetch_data()
#     print(df)
