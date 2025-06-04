from pydantic import BaseModel

class OrdersViewModel(BaseModel):
    itens: list
    total: float
    user_id: str
    restaurant: str
    status: str
    created_at: str
    updated_at: str