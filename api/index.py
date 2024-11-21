from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Email configuration
SMTP_SERVER = "smtp.gmail.com"  # Change if you're using another service
SMTP_PORT = 587
EMAIL_ADDRESS = "wkwong.ca@gmail.com"
EMAIL_PASSWORD = "hxhu xrpk hxwl dcxq"

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "HelloWorld"})

@app.route('/sendemail', methods=['POST'])
def sendemail():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    recipient = data.get('to')
    subject = data.get('subject')
    message_body = data.get('message')

    if not recipient or not subject or not message_body:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Create the email
        message = MIMEMultipart()
        message['From'] = EMAIL_ADDRESS
        message['To'] = recipient
        message['Subject'] = subject
        message.attach(MIMEText(message_body, 'html'))

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)

        return jsonify({"message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/helloworld', methods=['GET'])
def helloworld():
    return jsonify({"message": "Hell0 W0rld!"})

if __name__ == '__main__':
    app.run(debug=True)
