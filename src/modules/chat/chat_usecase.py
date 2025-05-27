import os
from bson import ObjectId
from pymongo import MongoClient
from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_viewmodel import ChatViewModel
from src.shared.entities.message import Message

class ChatUseCase:
    def __init__(self, repo: ChatRepository):
        self.repo = repo
        self.client = MongoClient(os.getenv("MONGODB_URL")) 
        self.database = self.client[os.getenv("DATABASE_NAME")]
        self.messages = self.database["messages"]
        self.users = self.database["users"]
        
    def chat(self, data: dict):
        try:
            restaurant_id = ObjectId(data["restaurant"])
            user_id = ObjectId(data["user_id"])

            restaurant_exists = self.users.find_one({"_id": restaurant_id})
            if not restaurant_exists:
                raise ValueError("Restaurante não encontrado.")

            user_exists = self.users.find_one({"_id": user_id})
            if not user_exists:
                raise ValueError("Usuário não encontrado.")

            message = Message(
                message=data["message"],
                restaurant=str(restaurant_id),
                user_id=str(user_id),
                type="human"
            )
            ai_message = self.repo.chat(message=message.message, user_id=message.user_id, restaurant=message.restaurant)

            ai_message_entity = Message(
                message=ai_message["message"],
                menu=ai_message["menu"],
                order=ai_message["order"],
                restaurant=ai_message["restaurant"],
                user_id=ai_message["user_id"],
                type="ai",

            )
            ai_viewmodel = ChatViewModel(
                message=ai_message_entity.message,
                menu=ai_message_entity.menu,
                order=ai_message_entity.order,
                restaurant=ai_message_entity.restaurant,
                user_id=ai_message_entity.user_id,
                type=ai_message_entity.type,
                )

            human_viewmodel = ChatViewModel(
                message=message.message,
                restaurant=message.restaurant,
                user_id=message.user_id,
                type="human",
                created_at=message.created_at,
                updated_at=message.updated_at
            )

            ai_model = ai_viewmodel.model_dump(mode='json')
            human_model = human_viewmodel.model_dump(mode='json')

            result = self.messages.insert_one(ai_model)
            self.messages.insert_one(human_model)

            ai_model["_id"] = str(result.inserted_id)
            return ai_model
        except Exception as e:
            raise e

        
    def history(self, user_id: str, restaurant: str):
        try:
            history = self.repo.history(user_id=user_id, restaurant=restaurant)
            return [{
                **message,
                "_id": str(message["_id"]),
            } for message in history]
        except Exception as e:
            raise e