from datetime import datetime, timedelta, timezone
import os
from src.modules.users.users_viewmodel import UsersViewModel
from src.shared.entities.user import User
from src.modules.users.users_repository import UsersRepository
import bcrypt
import jwt

class UsersUseCase:
    def __init__(self, repo: UsersRepository):
        self.repo = repo
        self.secret_key = os.getenv("SECRET_KEY")

    def create(self, data: dict):
        password = data["password"]
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        try:
            user = User(
                admin=False,
                email=data["email"],
                name=data["name"],
                phone=data["phone"],
                password_hash=hashed_password,
                restaurant=data["restaurant"],
                image=data["image"],
            )
            self.repo.create(user=user.model_dump())

            viewmodel = UsersViewModel(
                admin=user.admin,
                email=user.email,
                name=user.name,
                phone=user.phone,
                password_hash=hashed_password,
                restaurant=False,
                created_at=user.created_at,
                updated_at=user.updated_at
            )

            return viewmodel.model_dump_json()
        except Exception as e:
            raise e
    
    
    def delete(self, email: str):
        try:
            self.repo.delete(email)
            return {"message": "Usuário deletado com sucesso"}
        except Exception as e:
            raise e
    
    def update(self, email: str, data: dict):
        try:
            
            self.repo.update(email, data)
            return {"message": "Usuário atualizado com sucesso"}
        except Exception as e:
            raise e
        
    def update_schedule(self, email, day, open_time=None, close_time=None):
        user = self.repo.users.find_one({"email": email})
        if not user or not user.get("restaurant"):
            raise Exception("Restaurante não encontrado.")
        restaurant_id = user["_id"]
        return self.repo.update_schedule(restaurant_id, day, open_time, close_time)
    
    def get_all(self):
        return self.repo.get_all()

    def get_by_email(self, email):
        user = self.repo.get_by_email(email)
        if not user:
            raise Exception("Usuário não encontrado")
        return user

    def get_restaurants(self):
        return self.repo.get_restaurants()

    def login(self, email: str, password: str):
        user = self.repo.get_user_to_login(email)
        if not user:
            raise Exception("Usuário não encontrado")
        
        if not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
            raise Exception("Senha incorreta")
        
        payload = {
            "sub": user["_id"],
            "name": user["name"],
            "email": user["email"],
            "restaurant": user["restaurant"],
            "exp": datetime.now(timezone.utc) + timedelta(minutes=1440)
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        print(token)
        return {"token": token}
    
    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return { "valid": True }
        except jwt.ExpiredSignatureError:
            return { "valid": False }
        except jwt.InvalidTokenError:
            return { "valid": False }