from .db_service import test_conn
from .email_service import sendemail
from .user_service import register

def sendtimesheetemail(data):
    return sendemail(data)

def sayhelloworld():
    return test_conn()

def registeruser(data):
    return register(data)