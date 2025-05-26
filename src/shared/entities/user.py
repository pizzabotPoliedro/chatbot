from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    phone: int
    password_hash: bytes
    restaurant: bool
    admin: bool
    image: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
