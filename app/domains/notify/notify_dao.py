import json
from typing import List, Mapping, Dict

from fastapi import HTTPException

from app.domains.notify import UserDevicePayload, MessagePayload, Response
from app.conn.db import user_devices
from app.conn import db_manager
from app.clients.fcm import fcm_svc
from app.domains.notify.notify_dto import ErrorResponse


async def save(user_device: UserDevicePayload) -> Dict:
    last_record_id = await db_manager.save(user_devices, user_device)

    return {**user_device.dict(), "id": last_record_id}


async def get_tokens(user_id) -> List[Mapping]:
    tokens = await db_manager.get_tokens(user_devices, user_id)

    return tokens


async def send(message: MessagePayload) -> Response:
    tokens = await get_tokens(message.user_id)
    converted_tokens = [value for (value,) in tokens]

    if len(converted_tokens) == 0:
        raise HTTPException(status_code=404,
                            detail=f'user id {message.user_id} don\'t have any registered device(s)')

    batch_response = fcm_svc.send(message.message,
                                  message.notify.get("title"),
                                  message.notify.get("body"),
                                  converted_tokens
                                  )
    errors_lst = []
    for v in batch_response.responses:
        if v.exception:
            error = {}
            cause_resp = v.exception.__dict__.get("_cause").__dict__
            cause_dict = json.loads(cause_resp.get("content").decode('utf-8'))
            # Preparing custom error response list
            error["status"] = cause_dict.get("error").get("status", None)
            error["code"] = cause_dict.get("error").get("code", None)
            error["error_code"] = cause_dict.get("error").get("details")[0].get('errorCode', None)
            error["cause"] = cause_dict.get("error").get("message", None)
            errors_lst.append(error)

    resp = Response(
        success_count=batch_response.success_count,
        message=f"sent message to {batch_response.success_count} device(s)",
        error=ErrorResponse(
            count=batch_response.failure_count,
            errors=errors_lst
        )
    )

    return resp
