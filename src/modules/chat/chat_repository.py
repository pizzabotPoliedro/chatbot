import os
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
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
        
        self.menu = """
        Cardápio:
        - **Margherita**: Molho de tomate, mussarela e manjericão fresco.
        - **Pepperoni**: Molho de tomate, mussarela e fatias de pepperoni.
        - **Quatro Queijos**: Molho de tomate, mussarela, parmesão, gorgonzola e provolone.
        - **Vegetariana**: Molho de tomate, mussarela, pimentão, cebola, champignon e azeitonas.
        - **Calabresa**: Molho de tomate, mussarela, calabresa fatiada e cebola.
        - **Frango com Catupiry**: Molho de tomate, mussarela, frango desfiado e catupiry.
        - **Portuguesa**: Molho de tomate, mussarela, presunto, ovo, cebola, pimentão e azeitonas.
        - **Havaiana**: Molho de tomate, mussarela, presunto e abacaxi.
        - **Mexicana**: Molho de tomate, mussarela, carne moída temperada, pimenta jalapeño e cebola.
        - **Doce de Chocolate com Morango**: Chocolate derretido, morangos frescos e açúcar de confeiteiro.
        """

        self.horarios_de_funcionamento = """
        Horários de funcionamento:
        - Segunda-Feira: 17:00 às 23:00
        - Terça-Feira: 17:00 às 23:00
        - Quarta-Feira: 17:00 às 23:00
        - Quinta-Feira: 17:00 às 23:00
        - Sexta-Feira: 17:00 às 02:00
        - Sábado-Feira: 17:00 às 02:00
        - Domingo-Feira: 17:00 às 02:00
        """

        self.faq = """
        Dúvidas comuns:
        - Qual o nome do restaurante? -> Resposta: O nome do restaurante é TesteRestaurante
        - Qual seu nome? -> Resposta: RestauranteBot Poliedro
        - Quem é você? -> Resposta: Sou o RestauranteBot Poliedro, um robô inteligente responsável por tirar as dúvidas dos clientes sobre o restaurante {nome do restaurante aqui}!
        """

        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=self.openai_api_key,
            openai_api_base=self.openai_api_base,
        )

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
            SystemMessage(content=f"""
                Você é um assistente de um restaurante, que não consegue anotar pedidos nem realizar encomendas de pedidos ou algo do tipo, você apenas responde as dúvidas dos clientes sobre o restaurante.
                Aqui está o cardápio atual: {self.menu}.
                Aqui estão os horários de funcionamento: {self.horarios_de_funcionamento}.
                Aqui estão as perguntas mais comuns dos clientes seguidas de suas respectivas respostas: {self.faq}
            """)
        ] + history + [
            HumanMessage(content=message)
        ]

        response = self.llm.invoke(messages)

        return {
            "message": response.content,
            "user_id": user_id,
            "order": False,
            "menu": False,
            "restaurant": restaurant,
            "type": "ai",
        }
    
    def history(self, user_id: str, restaurant: str):
        return list(self.messages.find(
            {"user_id": user_id, "restaurant": restaurant}
        ).sort("created_at", -1))