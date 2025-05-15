from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_viewmodel import ChatViewModel
from src.shared.entities.message import Message

class ChatUseCase:
    def __init__(self, repo: ChatRepository):
        self.repo = repo

    def __call__(self, data: dict):
        try:
            message = Message(message=data["message"], session_id=data["session_id"], restaurant=data["restaurant"], user_id=data["user_id"], type="human")
            ai_message = self.repo.chat(message=message.message, session_id=message.session_id)
            viewmodel = ChatViewModel(message=ai_message, session_id=message.session_id, restaurant=message.restaurant, user_id=message.user_id, type="ai", created_at=message.created_at, updated_at=message.updated_at)
            return viewmodel.model_dump_json()
        except Exception as e:
            raise e