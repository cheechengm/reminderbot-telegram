import os
from pymongo import MongoClient

# 1. Try to load dotenv for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If it fails (like on Render), we just skip it 
    # because the variables are already in the environment.
    pass

# 2. Get the URL from environment variables
# Use a default or a check to make sure it exists
mongo_url = os.getenv("MONGO_URL")

if not mongo_url:
    # This helps you debug if you forgot to set the variable in Render
    raise ValueError("No MONGO_URL found in environment variables!")

# 3. Connect to MongoDB
client = MongoClient(mongo_url)
db = client["reminderbot"]
reminders = db["reminders"]