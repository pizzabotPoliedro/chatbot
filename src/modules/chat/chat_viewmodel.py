from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from src.shared.enums.type import Type

brt = timezone(timedelta(hours=-3))

class ChatViewModel(BaseModel):
    type: Type
    message: str
    restaurant: str
    user_id: str
    order: bool = False
    menu: bool = False
    schedule: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(brt))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(brt))

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
