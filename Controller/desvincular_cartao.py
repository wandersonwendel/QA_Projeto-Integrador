import pika

class MensagemDesvinculacaoCartao:
    def __init__(self, email, numero_cartao):
        self.email = email
        self.numero_cartao = numero_cartao

    def enviar(self):
        # Conectar ao RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()

        # Publicar a mensagem na fila
        channel.basic_publish(exchange='', routing_key='fila_desvincular_cartao', body=self.to_string())

        print(f'Solicitação de desvinculação de cartão enviada: {self.to_string()}')

        connection.close()

    def to_string(self):
        return f"{self.email};{self.numero_cartao}"


mensagem = MensagemDesvinculacaoCartao('wandersonsousa489@gmail.com', '1234567890123456')
mensagem.enviar()
