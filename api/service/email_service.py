import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

# Email configuration
def sendemail(request):
    SMTP_SERVER = "smtp.gmail.com"  # Change if you're using another service
    SMTP_PORT = 587
    EMAIL_ADDRESS = "wkwong.ca@gmail.com"
    EMAIL_PASSWORD = "hxhu xrpk hxwl dcxq"

    print(request)
    name = request.get('name')
    partner = request.get('partner')
    workfrom = request.get('workfrom')
    workto = request.get('workto')
    trucknum = request.get('truncknum')
    hadlunch = request.get('hadlunch')
    numofbreaks = request.get('numofbreaks')
    remarks = request.get('remarks')
    time_diff = workto-workfrom
    time_diff -= timedelta(minutes=30) if hadlunch else 0
    total_seconds = time_diff.total_seconds()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60


    message_body = workfrom.strftime("%d-%b-%Y %A")
    message_body += '<br />'
    message_body += f'{workfrom.strftime("%H%M")}-{workto.strftime("%H%M")}'
    message_body += '<br />'
    message_body += f'Truck: {trucknum}'
    message_body += f'{partner} {"WITH" if hadlunch else "NO"} Lunch'
    message_body += '<br />' 
    message_body += f'{hours} Hours {minutes} Minutes'
    message_body += '<br />' 
    message_body += f'Remarks: {remarks}'

    recipient = 'kentwkwong@gmail.com'
    subject = f'{name} Timesheet {workfrom.strftime("%y%m%d")}'
    message_body = message_body

    if not recipient or not subject or not message_body:
        return {"message": "E! Missing required fields", "code": 400}

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
        return {"message": f'ERROR!!! {str(e)}', "code": 500}


def sendemailsample(request):
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
