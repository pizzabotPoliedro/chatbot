import os
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient

class ChatRepository:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        self.openai_api_base = os.getenv("OPENROUTER_URL")
        self.model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))

        self.client = MongoClient(os.getenv("MONGODB_URL")) 
        self.database = self.client[os.getenv("DATABASE_NAME")]
        self.messages = self.database["messages"]

        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=self.openai_api_key,
            openai_api_base=self.openai_api_base,
        )

    def detect_intent(self, message):
        prompt = ChatPromptTemplate.from_template("""
            Analise a mensagem do usuário e responda apenas com uma das opções abaixo:
            - menu: se o usuário quer ver o cardápio, menu, lista de pratos ou bebidas.
            - order: se o usuário quer fazer um pedido, solicitar um prato, bebida ou algo do cardápio.
            - schedule: se o usuário está perguntando sobre o horário de funcionamento, abertura, fechamento ou dias em que o restaurante está aberto.
            - other: para qualquer outra intenção.

            Responda apenas com: menu, order, schedule ou other.
            Mensagem do usuário: "{message}"
        """)
        chain = prompt | self.llm
        result = chain.invoke({"message": message})
        intent = result.content.strip().lower()
        if intent not in ["menu", "order", "schedule"]:
            intent = "other"
        return intent

    def chat(self, message, user_id, restaurant):
        all_history = self.history(user_id, restaurant)
        history = []
        sorted_msgs = sorted(all_history, key=lambda x: x["created_at"])
        for msg in sorted_msgs:
            if msg["type"] == "human":
                history.append(HumanMessage(content=msg["message"]))
            elif msg["type"] == "ai":
                history.append(AIMessage(content=msg["message"]))

        messages = [
            SystemMessage(content="Você é um assistente de um restaurante. Caso o usuário pergunte sobre o cardápio ou sobre horários de funcionamento, diga que um modal será aberto na tela dele, para ele visualizar.")
        ] + history + [
            HumanMessage(content=message)
        ]

        response = self.llm.invoke(messages)

        intent = self.detect_intent(message)
        is_menu = intent == "menu"
        is_order = intent == "order"
        is_schedule = intent == "schedule"

        return {
            "message": response.content,
            "user_id": user_id,
            "order": is_order,
            "menu": is_menu,
            "schedule": is_schedule,
            "restaurant": restaurant,
            "type": "ai",
        }

    def history(self, user_id: str, restaurant: str):
        return list(self.messages.find(
            {"user_id": user_id, "restaurant": restaurant}
        ).sort("created_at", -1))
