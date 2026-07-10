from pydantic import BaseModel, IPvAnyAddress
from datetime import datetime

class DeviceCreate(BaseModel):
    name: str
    type: str
    ip_address: IPvAnyAddress
    port: int = 443
    username: str
    password: str

class DeviceResponse(BaseModel):
    id: int
    name: str
    type: str
    ip_address: str
    port: int
    version: str | None
    status: str
    username: str | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}