from typing import Dict, Optional, List
from pydantic import BaseModel, Field


class UserDevice(BaseModel):
    id: int
    user_id: int
    token: str
    device_info: Optional[Dict]


class UserDevicePayload(BaseModel):
    user_id: int = Field(..., gt=0, description="user_id must be greater than 0")
    token: str
    device_info: Optional[Dict]


class ErrorResponse(BaseModel):
    count: int = 0
    errors: Optional[List[Dict]]


class Response(BaseModel):
    success_count: int
    message: str
    error: ErrorResponse


class MessagePayload(BaseModel):
    user_id: int = Field(..., gt=0, description="user_id must be greater than 0")
    message: str
    notify: Dict
