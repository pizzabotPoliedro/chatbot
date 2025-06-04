from flask import Blueprint

from modules.orders.orders_repository import OrdersRepository
from modules.orders.orders_usecase import OrdersUseCase

orders_bp = Blueprint('orders', __name__)

@order_bp.route('/', methods=['GET'])
def make_order():
    repository = OrdersRepository()
    usecase = OrdersUseCase(repository)
    result = usecase()

    return result, 200

