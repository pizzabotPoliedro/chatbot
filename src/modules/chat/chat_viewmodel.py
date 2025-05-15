from dataclasses import Field
from datetime import datetime, timezone
from pydantic import BaseModel
from src.shared.enums.type import Type

class ChatViewModel(BaseModel):
    type: Type
    message: str
    session_id: str
    restaurant: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))