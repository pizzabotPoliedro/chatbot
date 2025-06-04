from modules.orders.orders_repository import OrdersRepository

class OrdersUseCase:
    def __init__(self, repo: OrdersRepository):
        self.repo = repo

    