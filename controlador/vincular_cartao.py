import pika
from model import Cartao

class RabbitMQManager:
    def __init__(self, host='localhost', port=5672):
        self.host = host
        self.port = port

    def enviar_mensagem(self, queue, mensagem):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
            channel = connection.channel()

            channel.basic_publish(exchange='', routing_key=queue, body=mensagem)

            print(f'Mensagem enviada para a fila {queue}: {mensagem}')

            connection.close()

        except Exception as e:
            print(f"Ocorreu um erro ao conectar-se ao RabbitMQ: {e}")

class CartaoManager:
    def vincular_cartao(self, email, numero_cartao, nome_titular, data_validade, cvv):
        mensagem = f"{email};{numero_cartao};{nome_titular};{data_validade};{cvv}"
        rabbitmq_manager = RabbitMQManager()

        rabbitmq_manager.enviar_mensagem('fila_vincular_cartao', mensagem)

        print(f'Solicitação de vinculação de cartão enviada: {mensagem}')

# Exemplos de uso
cartao_manager = CartaoManager()
cartao_manager.vincular_cartao('wandersonsousa489@gmail.com', '1234567890123456', 'Wanderson', '12/23', '123')