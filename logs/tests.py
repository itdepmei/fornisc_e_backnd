from django.test import TestCase

# Create your tests here.
import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forensicapp.settings')  # <-- Replace with your project name
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import os

# Only initialize once

# Only initialize once
if not firebase_admin._apps:
    cred_path = r"C:\Users\Lenovo\Desktop\forensic-backend\forensic\fernsic-ab3fb-firebase-adminsdk-fbsvc-6b5fc20934.json"
    cred = credentials.Certificate(cred_path)

    # cred = credentials.Certificate("fernsic-ab3fb-firebase-adminsdk-fbsvc-6b5fc20934.json")
    firebase_admin.initialize_app(cred)
    print("Firebase initialized!")

# Create your tests here.
# ...existing code...

def send_test_notification():
    """
    Send a test notification to a hardcoded device token for development.
    """
    test_token = "fea8aGKiTm2ndxD3Z0cfES:APA91bFkf9GyZYC9AmPVKrBDQOnNLiqrIkmENIbPRzQvfZYcC5qC_L6OiSJsXwXbf1Deypl-7123VSNo8F_Gws4zoPOokmp-33oq24jAqLVqGvsAkz6lfw4"
    title = "Test Notification"
    message = "This is a test notification from development."
    data = {
        "customKey": "customValue",
        "env": "development"
    }
    msg = messaging.Message(
        notification=messaging.Notification(title=title, body=message),
        data=data,
        token=test_token,
    )
    response = messaging.send(msg)
    print("Test notification sent. Response:", response)

# To run the test, you can call send_test_notification() from your main or Django shell.
# Example:
# >>> from logs.utils import firebase
send_test_notification()