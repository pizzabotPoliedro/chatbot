from flask import Blueprint, request

from src.modules.users.users_repository import UsersRepository
from src.modules.users.users_usecase import UsersUseCase


users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['POST'])
def create_user():
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    result = usecase.create(data=request.get_json())
    
    status_code = 200
    return result, status_code