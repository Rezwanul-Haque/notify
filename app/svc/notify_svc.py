from app.domains.notify import UserDevicePayload, MessagePayload
from app.domains import notify


async def register_device(user_device: UserDevicePayload):
    return await notify.save(user_device)


async def send_message(message: MessagePayload):
    success_count = await notify.send(message)

    return success_count
