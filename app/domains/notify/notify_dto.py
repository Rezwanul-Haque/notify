from typing import Dict, Optional
from pydantic import BaseModel


class UserDevice(BaseModel):
    id: int
    user_id: int
    token: str
    device_info: Optional[Dict]


class UserDevicePayload(BaseModel):
    user_id: int
    token: str
    device_info: Optional[Dict]


class Response(BaseModel):
    success_count: int
    message: str


class MessagePayload(BaseModel):
    user_id: int
    message: str
    notify: Dict
