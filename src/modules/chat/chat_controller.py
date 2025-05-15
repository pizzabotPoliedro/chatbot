from flask import Blueprint, request
from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_usecase import ChatUseCase

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat_check():
    repository = ChatRepository()
    usecase = ChatUseCase(repository)
    result = usecase(request.get_json())
    
    status_code = 200
    return result, status_code