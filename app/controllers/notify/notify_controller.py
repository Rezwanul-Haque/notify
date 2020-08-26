from fastapi import APIRouter

from app.domains.notify import UserDevice, UserDevicePayload, Response, MessagePayload
from app.svc import notify_svc

notify = APIRouter()


@notify.post("/v1/register", response_model=UserDevice, status_code=201)
async def register(payload: UserDevicePayload):
    return await notify_svc.register_device(payload)


@notify.post("/v1/message", response_model=Response, status_code=201)
async def send_message(payload: MessagePayload):
    res = await notify_svc.send_message(payload)

    return res
