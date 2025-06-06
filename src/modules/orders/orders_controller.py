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

@orders_bp.route('/orders/<user_id>', methods=['GET'])
def get_order_by_user_id(user_id):
    repository = OrdersRepository()
    usecase = OrdersUseCase(repository)
    result = usecase.get_order_by_user(user_id)

    return result, 200

@orders_bp.route('/orders/restaurant/<restaurant_id>', methods=['GET'])
def get_order_by_restaurant_id(restaurant_id):
    repository = OrdersRepository()
    usecase = OrdersUseCase(repository)
    result = usecase.get_order_by_restaurant(restaurant_id)

    return result, 200

@orders_bp.route('/orders/<order_id>/status', methods=['PUT'])
def set_order_status(order_id):
    status = request.json.get('status')
    if not status:
        return {"error": "O status é obrigatório!"}, 400

    repository = OrdersRepository()
    usecase = OrdersUseCase(repository)
    result = usecase.set_order_status(order_id, status)

    return result, 200