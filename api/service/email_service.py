import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import os

# Email configuration
def sendemail(request):
    SMTP_SERVER = "smtp.gmail.com"  # Change if you're using another service
    SMTP_PORT = 587
    EMAIL_ADDRESS = os.getenv('TIME_SHEET_FROM')
    EMAIL_PASSWORD = os.getenv('TIME_SHEET_FROM_CODE')

    # recipient_to = os.getenv('TIME_SHEET_TO')
    recipient_to = request.get('email')
    recipient_cc = request.get('email')
    print(recipient_cc)
    name = request.get('name')
    partner = request.get('partner')
    workfrom = request.get('from')
    workfrom = datetime.strptime(workfrom, "%Y-%m-%dT%H:%M")
    workto = request.get('to')
    workto = datetime.strptime(workto, "%Y-%m-%dT%H:%M")
    trucknum = request.get('truck')
    hadlunch = request.get('lunch')
    breaksCount = int(request.get('break'))
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

    try:
        # Create the email
        message = MIMEMultipart()
        message['From'] = EMAIL_ADDRESS
        message['To'] = recipient_to
        message['Cc'] = recipient_cc
        message['Subject'] = subject
        message.attach(MIMEText(message_body, 'html'))
        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)
        return {"result": "Email sent successfully!"}

    except Exception as e:
        return {"error": str(e)}

