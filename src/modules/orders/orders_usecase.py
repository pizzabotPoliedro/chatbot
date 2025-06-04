from src.modules.orders.orders_repository import OrdersRepository

class OrdersUseCase:
    def __init__(self, repo: OrdersRepository):
        self.repo = repo
    
    def make_order(self, order: dict):
        try:
            order_data = self.repo.make_order(order)
            return order_data
        except Exception as e:
            raise Exception(f"Erro ao fazer pedido: {str(e)}")

    