from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


EventType = Literal["click", "save", "apply"]


class FeedbackEventCreate(BaseModel):
    user_id: int
    job_id: int
    event_type: EventType


class FeedbackEventResponse(BaseModel):
    id: int
    user_id: int
    job_id: int
    event_type: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

