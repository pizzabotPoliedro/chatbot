from src.modules.orders.orders_repository import OrdersRepository

class OrdersUseCase:
    def __init__(self, repo: OrdersRepository):
        self.repo = repo
    
    def make_order(self, order: dict):
        try:
            order_data = self.repo.make_order(order)
            order_data["_id"] = str(order_data["_id"])
            return order_data
        except Exception as e:
            raise Exception(f"Erro ao fazer pedido: {str(e)}")

    def get_order_by_user(self, user_id: str, restaurant_id: str = None):
        try:
            order = self.repo.get_order_by_user(user_id, restaurant_id)
            for o in order:
                o["_id"] = str(o["_id"])
            return order
        except Exception as e:
            raise Exception(f"Erro ao obter pedidos: {str(e)}")
        
    def get_order_by_restaurant(self, restaurant_id: str):
        try:
            order = self.repo.get_order_by_restaurant(restaurant_id)
            for o in order:
                o["_id"] = str(o["_id"])
            return order
        except Exception as e:
            raise Exception(f"Erro ao obter pedidos: {str(e)}")
        
    def set_order_status(self, order_id: str, status: str):
        try:
            updated_order = self.repo.set_order_status(order_id, status)
            updated_order["_id"] = str(updated_order["_id"])
            return updated_order
        except Exception as e:
            raise Exception(f"Erro ao atualizar status do pedido: {str(e)}")
        
    