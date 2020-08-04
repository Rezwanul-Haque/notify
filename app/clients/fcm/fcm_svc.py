import logging

from typing import List
from firebase_admin import messaging, credentials, initialize_app

from app.config import get_settings


logger = logging.getLogger(__name__)


def init():
    cred = credentials.Certificate(cert=get_settings().messaging_credential_path)
    initialize_app(cred)


def send(msg: str, title: str, body: str, tokens: List[str]):
    notification = messaging.Notification(
        title=title,
        body=body
    )

    message = messaging.MulticastMessage(
        data={"message": msg},
        tokens=tokens,
        notification=notification
    )
    try:
        # ``dry_run`` mode is enabled, the message will not be actually delivered to the
        # recipients.Instead FCM performs all the usual validations, and emulates the send operation.
        response = messaging.send_multicast(message, dry_run=True)
        # See the BatchResponse reference documentation
        # for the contents of response.
        logger.info(f'{response.success_count} messages were sent successfully')
    except Exception as e:
        logger.exception("exception occur when sending message using firebase admin sdk")

    return response.success_count
