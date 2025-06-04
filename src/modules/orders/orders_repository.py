from datetime import datetime, timedelta, timezone
import os
from pymongo import MongoClient


class OrdersRepository:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URL")) 
        self.database = self.client[os.getenv("DATABASE_NAME")]
        self.users = self.database["users"]
        self.schedule = self.database["schedules"]
        self.items = self.database["items"]
        self.timezone = timezone(timedelta(hours=-3))
        self.orders = self.database["orders"]
    
    def calculate_total(self, order_items: list):
        total = 0.0
        for item in order_items:
            item_data = self.items.find_one({"_id": item["item_id"]})
            if item_data:
                total += item_data["item_price"] * item["quantity"]
            else:
                raise ValueError(f"Item {item['item_id']} não encontrado.")
        return total

    def make_order(self, order: dict):
        order_items = order["items"]
        order_restaurant_id = order["restaurant_id"]
        order_user_id = order["user_id"]

        restaurant_exists = self.users.find_one({"_id": order_restaurant_id})
        if not restaurant_exists:
            raise ValueError("Restaurante não encontrado.")
        
        user_exists = self.users.find_one({"_id": order_user_id})
        if not user_exists:
            raise ValueError("Usuário não encontrado.")
        
        for item in order_items:
            item_exists = self.items.find_one({"_id": item["item_id"], "restaurant_id": order_restaurant_id})
            if not item_exists:
                raise ValueError(f"Item {item['item_id']} não encontrado no restaurante {order_restaurant_id}.")
            
        order_data = {
            "items": order_items,
            "total": self.calculate_total(order_items),
            "user_id": order_user_id,
            "restaurant_id": order_restaurant_id,
            "status": "pending",
            "created_at": datetime.now(self.timezone),
        }

        self.orders.insert_one(order_data)
        
        return order_data
        