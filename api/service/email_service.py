import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os

# Email configuration
def sendemail(request):
    SMTP_SERVER = "smtp.gmail.com"  # Change if you're using another service
    SMTP_PORT = 587
    EMAIL_ADDRESS = "wkwong.ca@gmail.com"
    EMAIL_PASSWORD = "hxhu xrpk hxwl dcxq"

    print('-----------')
    # recipient_to = os.getenv('TIME_SHEET_TO')
    recipient_to = request.get('email')
    recipient_cc = request.get('email')
    print(recipient_cc)
    name = request.get('displayName')
    partner = request.get('partnerName')
    workfrom = request.get('workFrom')
    workfrom = datetime.strptime(workfrom, "%Y-%m-%dT%H:%M")
    workto = request.get('workTo')
    workto = datetime.strptime(workto, "%Y-%m-%dT%H:%M")
    trucknum = request.get('truckNum')
    hadlunch = request.get('hasLunch')
    breaksCount = int(request.get('breaksCount'))
    remarks = request.get('remarks')
    time_diff = workto-workfrom
    time_diff = time_diff - timedelta(minutes=30) if hadlunch else time_diff
    total_seconds = time_diff.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)


    message_body = workfrom.strftime("%d-%b-%Y %A")
    message_body += '<br />'
    message_body += f'{workfrom.strftime("%H%M")}-{workto.strftime("%H%M")}'
    message_body += '<br />'
    message_body += f'Truck {trucknum}'
    message_body += '<br />'
    message_body += f'{partner} {"WITH" if hadlunch else "NO"} Lunch'
    message_body += '<br />' 
    if (breaksCount > 0):
        message_body += f'Break: {breaksCount}'
        message_body += '<br />'
    message_body += f'{hours} Hours {minutes} Minutes'
    message_body += '<br />' 
    if (remarks != ""):
        message_body += f'Remarks: {remarks}'

    message_body += '<br />'
    message_body += '<br />'
    message_body += '<br />'
    message_body += '<br />'
    message_body += '<i>System generated email</i>'
    message_body += '<br />'


    subject = f'{name} Timesheet {workfrom.strftime("%y%m%d")}'
    print('1-----------')

    if not recipient_cc or not subject or not message_body:
        return {"message": "E! Missing required fields", "code": 400}

    try:
        # Create the email
        message = MIMEMultipart()
        message['From'] = EMAIL_ADDRESS
        message['To'] = recipient_to
        message['Cc'] = recipient_cc
        message['Subject'] = subject
        message.attach(MIMEText(message_body, 'html'))

        print('1-----------')
        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            print('2-----------')
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
            print('3-----------')
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
