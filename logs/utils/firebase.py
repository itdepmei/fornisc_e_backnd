import firebase_admin
from firebase_admin import credentials, messaging , exceptions
from django.conf import settings
import os
from ..models import Notification


# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("fernsic-ab3fb-firebase-adminsdk-fbsvc-6b5fc20934.json")
    firebase_admin.initialize_app(cred)



# Only i
# nitialize once
def send_notification_to_device(device_token, title, body, report_uuid, data=None):
    """
    Send a notification to a single device (first token in device_token list).
    Logs the notification in the database.
    """
    print("Sending notification to device ===========================>:", device_token)
    print("Title ==================>:", title)
    print("Body: ===================>:", body)
    print("Report UUID ===================>:", report_uuid)

    if not device_token or not isinstance(device_token, (list, tuple)):
        print("No device tokens provided.")
        return None

    target_token = device_token[0]
    notification_data = data or {report_uuid: report_uuid}

    msg = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        data=notification_data,
        token=target_token,
    )

    try:
        response = messaging.send(msg)
        print("Notification sent. Response:", response)

        Notification.objects.create(
            title=title,
            message=body,
            reportUuid=report_uuid
        )
        return response
    except exceptions.FirebaseError as e:
        print("FirebaseError:", e)
    except Exception as ex:
        print("Other error:", ex)
    return None

def send_notification_to_devices(device_tokens, title, body, report_uuid, data=None):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
        tokens=device_tokens,
    )
    try:
        response = messaging.send_multicast(message)
        print(f"✅ Successfully sent {response.success_count} messages")

        # Log to DB once per batch
    

        return response
    except exceptions.FirebaseError as e:
        print(" FirebaseError:", e)
    except Exception as ex:
        print(" Other error:", ex)


def send_notification_to_topic(topic, title, body, report_uuid, data=None):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
        topic=topic,
    )
    try:
        response = messaging.send(message)
        print("✅ Successfully sent message to topic:", response)

        Notification.objects.create(
            title=title,
            message=body,
            reportUuid=report_uuid
        )

        return response
    except exceptions.FirebaseError as e:
        print("❌ FirebaseError:", e)
    except Exception as ex:
        print("❌ Other error:", ex)