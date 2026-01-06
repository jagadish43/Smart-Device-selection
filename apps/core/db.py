from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["device_recommender"]

device_collection = db["devices"]
