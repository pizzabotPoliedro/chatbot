from flask import Blueprint, request
from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_usecase import ChatUseCase

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat_check():
    repository = ChatRepository()
    usecase = ChatUseCase(repository)
    result = usecase.chat(request.get_json())
    
    status_code = 200
    return result, status_code

@chat_bp.route('/chat', methods=['GET'])
def history():
    repository = ChatRepository()
    usecase = ChatUseCase(repository)
    
    data = request.get_json()
    if not data:
        return {"error": "Requisição deve conter JSON no corpo"}, 400
    
    user_id = data.get('user_id')
    restaurant = data.get('restaurant')
    
    if not user_id or not restaurant:
        return {"error": "user_id e restaurant são obrigatórios"}, 400
    
    try:
        result = usecase.history(user_id, restaurant)
        return {"messages": result}, 200 
    except Exception as e:
        return {"error": str(e)}, 500