from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_viewmodel import ChatViewModel
from src.shared.entities.message import Message

class ChatUseCase:
    def __init__(self, repo: ChatRepository):
        self.repo = repo

    def __call__(self, message: Message):
        try:
            ai_message = self.repo.chat(message=message.message, session_id=message.session_id)
            viewmodel = ChatViewModel()
            return viewmodel.model_dump_json()
        except Exception as e:
            raise e