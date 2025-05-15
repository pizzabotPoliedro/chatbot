from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
import os
class ChatRepository():
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_url = os.getenv("OPENROUTER_URL")
    model_name = os.getenv("MODEL_NAME")
    temperature = os.getenv("TEMPERATURE")
    menu = """
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

    horarios_de_funcionamento = """
        Horários de funcionamento:
        - Segunda-Feira: 17:00 às 23:00
        - Terça-Feira: 17:00 às 23:00
        - Quarta-Feira: 17:00 às 23:00
        - Quinta-Feira: 17:00 às 23:00
        - Sexta-Feira: 17:00 às 02:00
        - Sábado-Feira: 17:00 às 02:00
        - Domingo-Feira: 17:00 às 02:00
        """

    faq = """
        Dúvidas comuns:
        - Qual o nome do restaurante? -> Resposta: O nome do restaurante é TesteRestaurante
        - Qual seu nome? -> Resposta: RestauranteBot Poliedro
        - Quem é você? -> Resposta: Sou o RestauranteBot Poliedro, um robô inteligente responsável por tirar as dúvidas dos clientes sobre o restaurante {nome do restaurante aqui}!
        """

    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=openrouter_api_key,
        openai_api_base= openrouter_url
    )
    def chat(self, message, session_id):
        history = [HumanMessage("meu nome é matheus."), AIMessage("Entendido, vou te chamar de Matheus a partir de agora.")]

        messages = [
                SystemMessage(content=f"""
                Você é um assistente de um restaurante, que não consegue anotar pedidos nem realizar encomendas de pedidos ou algo do tipo, você apenas responde as dúvidas dos clientes sobre o restaurante.
                Aqui está o cardápio atual: {self.menu}.
                Aqui está os horários de funcionamento: {self.horarios_de_funcionamento}.
                Aqui está as perguntas mais comuns dos clientes seguido de sua devida resposta: {self.faq}""")
            ] + history + [
                HumanMessage(content=message)
            ]

        response = self.llm(messages)
        ai_message = response.content
        return ai_message