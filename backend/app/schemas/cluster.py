from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ClusterMemberCreate(BaseModel):
    device_id: int
    role: str
    priority: int = 100

class ClusterMemberResponse(BaseModel):
    id: int
    device_id: int
    role: str
    priority: int
    status: str

    model_config = {"from_attributes": True}

class ClusterCreate(BaseModel):
    name: str
    type: str

class ClusterResponse(BaseModel):
    id: int
    name: str
    type: str
    status: str
    members: List[ClusterMemberResponse]
    created_at: datetime

    model_config = {"from_attributes": True}