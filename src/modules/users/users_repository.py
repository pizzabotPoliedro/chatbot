import os
import bcrypt
from pymongo import MongoClient
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from bson.objectid import ObjectId
from src.shared.entities.user import User

class UsersRepository:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URL")) 
        self.database = self.client[os.getenv("DATABASE_NAME")]
        self.users = self.database["users"]
        self.schedule = self.database["schedules"]
        self.items = self.database["items"]

    def create(self, user: dict):
        email_exist = self.users.find_one({"email": user["email"]})

        if email_exist:
            raise Exception("Email já existe")
        
        
        created_user = self.users.insert_one(user)
        if user["restaurant"]:
            restaurant_schedule = {
                "restaurant_id": created_user.inserted_id,
                "monday": {
                    "open": None,
                    "close": None
                },
                "tuesday": {
                    "open": None,
                    "close": None
                },
                "wednesday": {
                    "open": None,
                    "close": None
                },
                "thursday": {
                    "open": None,
                    "close": None
                },
                "friday": {
                    "open": None,
                    "close": None
                },
                "saturday": {
                    "open": None,
                    "close": None
                },
                "sunday": {
                    "open": None,
                    "close": None
                }
            }
            self.schedule.insert_one(restaurant_schedule)
        return created_user
    
    def delete(self, email: str):
        user = self.users.find_one({"email": email})
        if not user:
            raise Exception("Usuário não encontrado")

        if user.get("restaurant"):
            self.schedule.delete_one({"restaurant_id": user["_id"]})

        result = self.users.delete_one({"email": email})
        if result.deleted_count == 0:
            raise Exception("Erro ao deletar usuário")
        return True
    
    def update(self, email: str, update_data: dict):
        user = self.users.find_one({"email": email})
        if not user:
            raise Exception("Usuário não encontrado")

        FIELDS_NOT_ALLOWED = ["email", "_id", "admin", "created_at", "updated_at", "restaurant"]
        forbidden_fields = [field for field in update_data if field in FIELDS_NOT_ALLOWED]
        if forbidden_fields:
            raise Exception(f"Não é permitido alterar os campos: {', '.join(forbidden_fields)}")

        if "password" in update_data:
            password = update_data.pop("password")
            password_bytes = password.encode("utf-8")
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password_bytes, salt)
            update_data["password_hash"] = hashed_password

        result = self.users.update_one(
            {"email": email},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise Exception("Erro ao atualizar usuário")
        return True
        
    def update_schedule(self, restaurant_id, day, open_time, close_time):
        update_fields = {
            f"{day}.open": open_time,
            f"{day}.close": close_time
        }
        
        result = self.schedule.update_one(
            {"restaurant_id": restaurant_id},
            {"$set": update_fields}
        )
        
        if result.matched_count == 0:
            raise Exception("Horário não encontrado para esse restaurante.")
        return True
    
    def get_all(self):
        users = list(self.users.find({}, {'password_hash': 0, 'image': 0}))
        for user in users:
            user['_id'] = str(user['_id'])
        return users

    def get_by_email(self, email):
        user = self.users.find_one({"email": email}, {'image': 0})
        if user:
            user['_id'] = str(user['_id'])
            user['password_hash'] = str(user['password_hash'])
        return user

    def get_restaurants(self):
        restaurants = list(self.users.find({"restaurant": True}, {'password_hash': 0, 'image': 0}))
        for restaurant in restaurants:
            restaurant['_id'] = str(restaurant['_id'])
        return restaurants

    def get_user_to_login(self, email):
        user = self.users.find_one({"email": email}, {'image': 0})
        if user:
            user['_id'] = str(user['_id'])
        return user
        
    def get_schedule_by_email(self, email: str):
        user = self.users.find_one({"email": email})
        
        
        schedule = self.schedule.find_one({"restaurant_id": user["_id"]})
        
        if not schedule:
            return None 
        
        schedule["_id"] = str(schedule["_id"])
        schedule["restaurant_id"] = str(schedule["restaurant_id"])
        
        return schedule

    def add_item_to_menu(self, item):
        add_item = self.items.insert_one(item)
        return True
    
    def delete_item(self, item_id):
        try:
            object_id = ObjectId(item_id)
        except:
            raise Exception("ID de item inválido")

        item = self.items.find_one({"_id": object_id})
        if not item:
            raise Exception("Item não encontrado")

        result = self.items.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            raise Exception("Erro ao deletar item")
        return {"message": "Item deletado com sucesso"}
    
    def get_menu(self, restaurant_id):

        items = list(self.items.find({"restaurant_id": restaurant_id}))
        for item in items:
            item["_id"] = str(item["_id"])
            if "image" in item and item["image"]:
                item["image"] = item["image"]
        
        if not items:
            raise Exception("Nenhum item encontrado para este restaurante")
        
        return {"items": items, "restaurant_id": restaurant_id}