import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.messaging import UnregisteredError
from notifications.models import Device
import os

if DEBUG is True:
    cred_path = os.path.join(os.path.dirname(__file__), "service-account.json")
else:
    cred_path = json.loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

def send_push(token, title, body):
    message = messaging.Message(
        token=token,
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        android=messaging.AndroidConfig(
            priority="high",
            notification=messaging.AndroidNotification(
                sound="default",
                channel_id="amparo_channel",
            ),
        ),
    )

    try:
        return messaging.send(message)

    except UnregisteredError:
        Device.objects.filter(fcm_token=token).delete()
        return "TOKEN_INVALIDO"
