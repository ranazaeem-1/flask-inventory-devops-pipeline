from pymongo import MongoClient
import sys

# Your actual MongoDB Atlas connection string
connection_string = 'mongodb+srv://abc:abc@cluster0.fu3wg2m.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

try:
    # Create a new client and connect to the server
    client = MongoClient(connection_string)
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("MongoDB Atlas connection successful!")
    
    # List available databases
    dbs = client.list_database_names()
    print("Available databases:", dbs)
    
except Exception as e:
    print(f"MongoDB Atlas connection error: {e}", file=sys.stderr)
    sys.exit(1)
