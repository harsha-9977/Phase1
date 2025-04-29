import pandas as pd
from pymongo import MongoClient

# Step 1: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["nowhere"]  # Your database name
collection = db["crimes"]  # Your collection name

# Step 2: Load CSV data
df = pd.read_csv("../data/crime.csv", encoding='latin1')  # or 'ISO-8859-1'

# Step 3: Drop missing values for required fields
df = df.dropna(subset=["HOUR", "MONTH", "DAY_OF_WEEK", "OFFENSE_CODE"])

# Step 4: Insert into MongoDB
collection.insert_many(df.to_dict(orient="records"))

print("✅ Crime data successfully inserted into MongoDB.")
