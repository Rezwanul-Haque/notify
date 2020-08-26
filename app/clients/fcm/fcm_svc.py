import logging
import json
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
        errors_lst = []
        for i in range(len(response.responses)):
            if response.responses[i] and response.responses[i].exception:
                error = {}
                cause_resp = response.responses[i].exception.__dict__.get("_cause").__dict__
                cause_dict = json.loads(cause_resp.get("content").decode('utf-8'))
                # Preparing custom error response list
                error["status"] = cause_dict.get("error").get("status", None)
                error["code"] = cause_dict.get("error").get("code", None)
                error["error_code"] = cause_dict.get("error").get("details")[0].get('errorCode', None)
                error["cause"] = cause_dict.get("error").get("message", None)
                errors_lst.append(error)

        logger.info(f'sent message to {response.success_count} device(s)')

        return {"success_count": response.success_count,
                "message": f'sent message to {response.success_count} device(s)',
                "error": {"count": response.failure_count, "message": errors_lst}
                }
    except Exception as e:
        logger.exception("exception occur when sending message using firebase admin sdk")


