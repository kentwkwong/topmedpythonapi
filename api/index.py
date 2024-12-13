from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from service import db_service, email_service, util_service
from bson import json_util

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "heeeeeeello world"})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = db_service.register(data)
    return jsonify(response), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = db_service.login(data["email"], data["password"])
    print(response)
    return jsonify(response), 200

@app.route('/verifypassword', methods=['POST'])
def verifypassword():
    data = request.get_json()
    password = data.get('password')
    hash = "$2b$12$Ul6tF6leOUc/6AZvHaA19eNpJZmVd91e3Naq8pvaocc9sF5y71T0q"
    result = db_service.verify_password(password, hash)
    return jsonify({"message":result}), 400

@app.route('/sendtimesheetemail', methods=['POST'])
def sendtimesheetemail():
    data = request.json
    ret = db_service.insert_timesheet(data)
    if ret != '':
        return jsonify({"message":ret}), 500
    
    user = db_service.get_user(data.get('displayName'))

    data['email'] = user['email']
    print(data)

    result = email_service.sendemail(data)
    return jsonify({"message":result.get("message")}), result.get("code")

@app.route('/getuser', methods=['GET'])
def get_user():
    result = db_service.get_user("Kent")
    print(result['email'])
    return util_service.return_json(result)
    

@app.route('/getalltimesheet', methods=['GET'])
def getalltimesheet():
    result = db_service.get_all_timesheet()
    json_results = json_util.dumps(result, indent=4) 
    print(json_results)
    return json_results

@app.route('/helloworld', methods=['GET'])
def helloworld():
    return jsonify({"message":"hard code helloworld"}), 400

if __name__ == '__main__':
    app.run(debug=True)

