import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "megebase_media_service")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "media")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]


def update_media_by_id(media_id: str, updated_data: dict) -> int:
    result = collection.update_one({"_id": media_id}, {"$set": updated_data})
    return result.modified_count
