from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variables
mongo_uri = os.environ.get('MONGO_URI')

if not mongo_uri:
    print("Error: MONGO_URI environment variable not set")
    exit(1)

try:
    # Connect to MongoDB
    print(f"Attempting to connect to MongoDB with URI: {mongo_uri[:20]}...")
    client = MongoClient(mongo_uri)
    
    # Test the connection
    print("Testing connection...")
    client.admin.command('ping')
    
    # List databases to further confirm connection
    print("Connection successful! Available databases:")
    dbs = client.list_database_names()
    for db in dbs:
        print(f" - {db}")
        
    print("\nMongoDB connection test successful!")
    
except Exception as e:
    print(f"Error: Failed to connect to MongoDB: {e}")
