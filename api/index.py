from flask import Flask, request, jsonify
# import email_service
# from pymongo import MongoClient

app = Flask(__name__)

# Email configuration
SMTP_SERVER = "smtp.gmail.com"  # Change if you're using another service
SMTP_PORT = 587
EMAIL_ADDRESS = "wkwong.ca@gmail.com"
EMAIL_PASSWORD = "hxhu xrpk hxwl dcxq"

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "HelloWorld"})

@app.route('/register', methods=['POST'])
def register():
    return {"message": "CORS working!"}, 200
    # data = request.get_json()
    # response = lib.user_service.register(data)
    # return jsonify(response), 400


@app.route('/sendingemail', methods=['POST'])
def sendingemail():
    return {"message": "CORS working!"}, 200 
    # result = email_service.sendemail(request.json)
    # return jsonify({"message":result.get("message")}), result.get("code")

@app.route('/helloworld', methods=['GET'])
def helloworld():
    return jsonify({"message":"hello world!"}), 400

if __name__ == '__main__':
    app.run(debug=True)
