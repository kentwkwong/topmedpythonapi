from pymongo import MongoClient
import os

db_conn = os.getenv('DB_CONNECTION_STRING')


client = MongoClient("mongodb://localhost:27017/")
client = MongoClient(db_conn)
db = client.topmed
users_collection = db.users

def register(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return {"message": "All fields are required!", "code": 400}

    if users_collection.find_one({"email": email}):
        return {"message": "User already exists!", "code": 400}

    users_collection.insert_one({"username": username, "email": email, "password": password})
    return {"message": "Registration successful!", "code": 201}