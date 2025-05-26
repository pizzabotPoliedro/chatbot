from pydantic import Field
from datetime import datetime
from pydantic import BaseModel
from src.shared.enums.type import Type

class ChatViewModel(BaseModel):
    type: Type
    message: str
    session_id: str
    restaurant: str
    user_id: str
    created_at: datetime
    updated_at: datetime