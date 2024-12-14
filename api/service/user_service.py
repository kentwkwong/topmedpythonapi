from pymongo import MongoClient
import os
import bcrypt
from bson import json_util

db_conn = os.getenv('DB_CONNECTION_STRING')

client = MongoClient(db_conn)
db = client["topmed"]
users_collection = db["users"]


def get_user(user):
    try:
        result = users_collection.find_one({"name":user})
        return result
    except Exception as e:
        return None
    

def login(email, password):
    try:
        result = users_collection.find_one({"email":email})
        if (result != None):
            chkpw = verify_password(password, result["password"] )
            if chkpw:
                return {"result":result["name"]}
            else:
                return {"error":"Invalid password"}
        else:
            return {"error":"Email not existed!"}
    except Exception as e:
        return {"error": str(e)}

def register(data):
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    password = hash_password(password)
    print(data)
    if not name or not email or not password:
        return {"error": "All fields are required!"}

    if users_collection.find_one({"email": email}):
        return {"error": "Email already exists!"}

    users_collection.insert_one({"name": name, "email": email, "password": password})
    return {"result": "Registration successful!"}

def hash_password(password: str) -> str:
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))
