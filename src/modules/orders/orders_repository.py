from datetime import datetime, timedelta, timezone
import os
from bson import ObjectId
from pymongo import MongoClient

from src.shared.enums.order_status import OrderStatus


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
            item_data = self.items.find_one({"_id": ObjectId(item["item_id"])})
            if item_data:
                total += float(item_data["price"]) * item["quantity"]
            else:
                raise ValueError(f"Item {item['item_id']} não encontrado.")
        return total

    def make_order(self, order: dict):
        order_items = order["items"]
        order_restaurant_id = order["restaurant_id"]
        order_user_id = order["user_id"]

        restaurant_exists = self.users.find_one({"_id": ObjectId(order_restaurant_id)})
        if not restaurant_exists:
            raise ValueError("Restaurante não encontrado.")
        
        user_exists = self.users.find_one({"_id": ObjectId(order_user_id)})
        if not user_exists:
            raise ValueError("Usuário não encontrado.")
        
        for item in order_items:
            item_exists = self.items.find_one({"_id": ObjectId(item["item_id"]), "restaurant_id": order_restaurant_id})
            if not item_exists:
                raise ValueError(f"Item {item['item_id']} não encontrado no restaurante {order_restaurant_id}.")
            
        order_data = {
            "items": order_items,
            "total": self.calculate_total(order_items),
            "user_id": str(order_user_id),
            "restaurant_id": str(order_restaurant_id),
            "status": OrderStatus.PENDING.value,
            "created_at": datetime.now(self.timezone.utc),
        }

        self.orders.insert_one(order_data)
        
        return order_data
    
    def get_order_by_user(self, user_id: str, restaurant_id: str = None):
        query = {"user_id": user_id}
        if restaurant_id:
            query["restaurant_id"] = restaurant_id
        
        orders_cursor = self.orders.find(query)
        orders = list(orders_cursor)
        
        for o in orders:
            o["_id"] = str(o["_id"])
        
        return orders

    def get_order_by_restaurant(self, restaurant_id: str):
        orders_cursor = self.orders.find({"restaurant_id": restaurant_id})
        orders = list(orders_cursor)

        for o in orders:
            o["_id"] = str(o["_id"])
        return orders
    
    def set_order_status(self, order_id: str, status: str):
        order_exists = self.orders.find_one({"_id": ObjectId(order_id)})

        result = self.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": status}}
        )
        order_exists = self.orders.find_one({"_id": ObjectId(order_id)})
        return order_exists
    
    def get_order_by_user_and_restaurant(self, user_id: str, restaurant_id: str):
        orders_cursor = self.orders.find({"user_id": user_id, "restaurant_id": restaurant_id})
        orders = list(orders_cursor)
        if not orders:
            raise ValueError("Pedidos não encontrados.")
        for o in orders:
            o["_id"] = str(o["_id"])
        return orders