from flask import Blueprint
from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_usecase import ChatUseCase

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat_check():
    repository = ChatRepository()
    usecase = ChatUseCase(repository)
    result = usecase()
    
    status_code = 200
    return result, status_code