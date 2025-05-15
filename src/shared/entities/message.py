from pydantic import BaseModel, Field
from datetime import datetime, timezone
from src.shared.enums.type import Type

class Message(BaseModel):
    type: Type
    message: str
    session_id: str
    restaurant: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))
