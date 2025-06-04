from flask import Blueprint, request

from src.modules.orders.orders_repository import OrdersRepository
from src.modules.orders.orders_usecase import OrdersUseCase

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['POST'])
def make_order():
    repository = OrdersRepository()
    usecase = OrdersUseCase(repository)
    result = usecase.make_order(request.json)

    return result, 200

