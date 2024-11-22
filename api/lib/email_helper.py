import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Email configuration


def sendemail(request):
    SMTP_SERVER = "smtp.gmail.com"  # Change if you're using another service
    SMTP_PORT = 587
    EMAIL_ADDRESS = "wkwong.ca@gmail.com"
    EMAIL_PASSWORD = "hxhu xrpk hxwl dcxq"

    print(request)
    
    recipient = request.get('to')
    subject = request.get('subject')
    message_body = request.get('message')

    if not recipient or not subject or not message_body:
        return {"error": "Missing required fields", "code": 400}

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

        return {"message": "Email sent successfully!", "code": 200}

    except Exception as e:
        return {"error": str(e), "code": 500}
