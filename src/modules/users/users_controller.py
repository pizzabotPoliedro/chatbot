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
        if data.get('restaurant') is not None:
            if data['restaurant'] == 'true' or data['restaurant'] == 'True':
                data['restaurant'] = True
            else:
                data['restaurant'] = False
        if data.get('admin') is not None:
            if data['admin'] == 'true' or data['admin'] == 'True':
                data['admin'] = True
            else:
                data['admin'] = False
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
    
@users_bp.route('/menu', methods=['POST'])
def add_item_to_menu():
    repository = UsersRepository()
    usecase = UsersUseCase(repository)

    data = request.form.to_dict()

    required_fields = ['name', 'price', 'description', 'restaurant_id']
    for field in required_fields:
        if field not in data or not data[field]:
            return {"error": f"Campo '{field}' é obrigatório"}, 400

    if 'image' in request.files:
        image_bytes = request.files['image'].read()
        data['image'] = image_to_base64(image_bytes)
    else:
        data['image'] = None

    item = {
        "name": data['name'],
        "price": data['price'],
        "description": data['description'],
        "image": data['image'],
        "restaurant_id": data['restaurant_id'],
        "active": True
    }

    try:
        result = usecase.add_item_to_menu(item)
        return {"message": "Item adicionado ao menu com sucesso"}, 201
    except Exception as e:
        return {"error": str(e)}, 400

@users_bp.route('/menu/<id>', methods=['DELETE'])
def delete_item(id):
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    result = usecase.delete_item(id)
    return result, 200

@users_bp.route('/menu/<id>', methods=['GET'])
def get_menu(id):
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    result = usecase.get_menu(id)
    return result, 200

@users_bp.route('/menu/active/<id>', methods=['PUT'])
def activate_item(id):
    repository = UsersRepository()
    usecase = UsersUseCase(repository)
    data = request.json

    if 'active' not in data:
        return {"error": "O campo 'active' é obrigatório"}, 400
    result = usecase.activate_item(id, data['active'])
    return result, 200

@users_bp.route('/menu/<restaurant_id>/activated', methods=['GET'])
def get_activated_menu(restaurant_id):
    repository = UsersRepository()
    usecase = UsersUseCase(repository)

    menu = usecase.get_activated_menu(restaurant_id)
    return menu, 200

