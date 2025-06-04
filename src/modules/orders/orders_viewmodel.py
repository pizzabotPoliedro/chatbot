from pydantic import BaseModel

class OrdersViewModel(BaseModel):
    itens: list
    total: float
    user_id: str
    restaurant_id: str
    status: str
    created_at: str
    updated_at: str