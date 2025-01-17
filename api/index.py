from flask import Flask, request, jsonify
from flask_cors import CORS
from bson import json_util
from .service import email_service, util_service, timesheet_service, user_service

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "heeeeeeello world"})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    response = user_service.register(data)
    return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    response = user_service.login(data["email"], data["password"])
    print(response)
    return jsonify(response)

@app.route('/sendtimesheetemail', methods=['POST'])
def sendtimesheetemail():
    data = request.json
    timesheet_service.insert_timesheet(data)   
    user = user_service.get_user(data.get('name'))
    data['email'] = user['email']
    data_with_hours = util_service.calculate_work_hours(data)
    response = email_service.sendemail(data_with_hours)
    return jsonify(response)


@app.route('/gettimesheetbyname', methods=['GET'])
def getalltimesheet():
    name = request.args.get('name')
    result = timesheet_service.get_timesheet_by_name(name)
    for item in result:
        item = util_service.calculate_work_hours(item)
    json_results = json_util.dumps(result, indent=4) 
    return json_results

@app.route('/getweeklytimesheetbyname', methods=['GET'])
def getweeklytimesheet():
    name = request.args.get('name')
    result = timesheet_service.get_timesheet_by_name(name)
    for item in result:
        item = util_service.calculate_work_hours(item)
    result = util_service.group_weekly_hours(result)
    json_results = json_util.dumps(result, indent=4) 
    return json_results

@app.route('/helloworld', methods=['GET'])
def helloworld():
    return jsonify({"message":"hard code helloworld"}), 200

if __name__ == '__main__':
    app.run(debug=True)

