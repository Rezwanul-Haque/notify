from app.domains.notify import UserDevicePayload, MessagePayload
from app.conn.db import user_devices
from app.conn import db_manager
from app.clients.fcm import fcm_svc


async def save(user_device: UserDevicePayload):
    last_record_id = await db_manager.save(user_devices, user_device)

    return {**user_device.dict(), "id": last_record_id}


async def get_tokens(user_id):
    tokens = await db_manager.get_tokens(user_devices, user_id)

    return tokens


async def send(message: MessagePayload):
    tokens = await get_tokens(message.user_id)
    converted_tokens = [value for (value,) in tokens]
    success_count = fcm_svc.send(message.message, message.notify.get("title"), message.notify.get("body"), converted_tokens)

    return success_count



