from pymongo import MongoClient
import os
import bcrypt
from bson import json_util

db_conn = os.getenv('DB_CONNECTION_STRING')
history_count = int(os.getenv('HISTORY_COUNT'))
print(type(history_count))
client = MongoClient(db_conn)
db = client["topmed"]
timesheet_collection = db["timesheets"]

def insert_timesheet(data):
    try:
        # Insert the JSON data into MongoDB
        if isinstance(data, list):
            result = timesheet_collection.insert_many(data)
        else:
            result = timesheet_collection.insert_one(data)
        return {"result":"Timesheet submitted successfully!"}
    except Exception as e:
        return {"error":e}


def get_timesheet_by_name(name):
    result = list(timesheet_collection.find({"name":name}).sort("from",-1).limit(history_count))
    return result

