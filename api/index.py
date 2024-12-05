from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from .service import db_service, email_service

app = Flask(__name__)
CORS(app)

# Email configuration
SMTP_SERVER = "smtp.gmail.com"  # Change if you're using another service
SMTP_PORT = 587
EMAIL_ADDRESS = "wkwong.ca@gmail.com"
EMAIL_PASSWORD = "hxhu xrpk hxwl dcxq"

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "heeeeeeello world"})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = db_service.register(data)
    return jsonify(response), 400

@app.route('/verifypassword', methods=['POST'])
def verifypassword():
    data = request.get_json()
    password = data.get('password')
    hash = "$2b$12$Ul6tF6leOUc/6AZvHaA19eNpJZmVd91e3Naq8pvaocc9sF5y71T0q"
    result = db_service.verify_password(password, hash)
    return jsonify({"message":result}), 400

@app.route('/sendtimesheetemail', methods=['POST'])
def sendtimesheetemail():
    result = email_service.sendemail(request.json)
    return jsonify({"message":result.get("message")}), result.get("code")

@app.route('/helloworld', methods=['GET'])
def helloworld():
    return jsonify({"message":"hard code helloworld"}), 400

if __name__ == '__main__':
    app.run(debug=True)
