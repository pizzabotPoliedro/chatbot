from datetime import datetime
from pydantic import BaseModel
from src.shared.enums.type import Type

class UsersViewModel(BaseModel):
    name: str
    email: str
    phone: int
    password_hash: str
    restaurant: bool
    admin: bool
    created_at: datetime
    updated_at: datetime