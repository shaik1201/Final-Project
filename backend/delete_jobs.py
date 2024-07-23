from pymongo import MongoClient
import config

try:
    client = MongoClient(config.MONGO_URI)
    db = client.job_search_db
    print("Connection to MongoDB successful")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

# Delete all documents in the jobs collection
db.jobs.delete_many({})

print("All records have been deleted.")