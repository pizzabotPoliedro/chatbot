from flask import Blueprint, jsonify, request

from src.shared.utils.image_to_base64 import image_to_base64
from src.modules.users.users_repository import UsersRepository
from src.modules.users.users_usecase import UsersUseCase


users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_all_users():
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    users = usecase.get_all()
    return jsonify(users), 200

@users_bp.route('/users/<email>', methods=['GET'])
def get_user_by_email(email):
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    try:
        user = usecase.get_by_email(email)
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@users_bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    restaurants = usecase.get_restaurants()
    return jsonify(restaurants), 200

@users_bp.route('/users', methods=['POST'])
def create_user():
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    data = request.form.to_dict()

    if "image" not in data:
        data["image"] = None

    if 'image' in request.files:
        image_bytes = request.files['image'].read()
        data["image"] = image_to_base64(image_bytes)
    else:
        data["image"] = None

    try:
        result = usecase.create(data=data)
        return {"success": True, "message": "Usuário criado com sucesso", "data": result}, 201
    except Exception as e:
        return {"success": False, "error": str(e)}, 400

@users_bp.route('/users/<email>', methods=['DELETE'])
def delete_user(email):
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    result = usecase.delete(email)
    return result, 200


@users_bp.route('/users/<email>', methods=['PUT'])
def update_user(email):
    repository = UsersRepository()
    usecase = UsersUseCase(repository)

    if request.content_type.startswith('multipart/form-data'):
        data = request.form.to_dict()
        if 'image' in request.files:
            image_bytes = request.files['image'].read()
            data['image'] = image_to_base64(image_bytes)
    else:
        data = request.get_json() or {}

    try:
        result = usecase.update(email, data)
        return result, 200
    except Exception as e:
        return {"error": str(e)}, 400

    
@users_bp.route('/users/<email>/schedule', methods=['PUT'])
def update_user_schedule(email):
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    data = request.json

    day = data.get("day")
    open_time = data.get("open")
    close_time = data.get("close")

    try:
        usecase.update_schedule(email, day, open_time, close_time)
        return {"message": "Horário atualizado com sucesso"}, 200
    except Exception as e:
        return {"error": str(e)}, 400
    
@users_bp.route('/login', methods=['POST'])
def login():
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    data = request.form.to_dict()
    email = data.get("email")
    password = data.get("password")

    try:
        token = usecase.login(email, password)
        return token, 200
    except Exception as e:
        return {"error": str(e)}, 400
    
@users_bp.route('/verify-token', methods=['POST'])
def token():
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    data = request.form.to_dict()
    token = data.get("token")

    try:
        token = usecase.verify_token(token)
        return token, 200
    except Exception as e:
        return {"error": str(e)}, 400
    
@users_bp.route('/signup', methods=['POST'])
def signup():
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    data = request.form.to_dict()

    if "image" not in data:
        data["image"] = None
        
    if 'image' in request.files:
        image_bytes = request.files['image'].read()
        data["image"] = image_to_base64(image_bytes)
    else:
        data["image"] = None

    try:
        result = usecase.create(data=data)
        return {"success": True, "message": "Usuário criado com sucesso", "data": result}, 201
    except Exception as e:
        return {"success": False, "error": str(e)}, 400
    
@users_bp.route('/users/<email>/schedule', methods=['GET'])
def get_schedule(email):
    repository = UsersRepository()
    usecase = UsersUseCase(repository)

    try:
        schedule = usecase.get_schedule(email)
        return schedule, 200
    except Exception as e:
        return {"error": str(e)}, 400
