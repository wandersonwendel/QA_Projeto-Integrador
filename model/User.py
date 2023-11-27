import pika

class User:
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    def enviar_login(self):
        mensagem = f"{self.email};{self.senha}"

        # Conectar ao RabbitMQ
        with pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672)) as connection:
            channel = connection.channel()

            # Publicar a mensagem na fila
            channel.basic_publish(exchange='', routing_key='fila_login_passageiro', body=mensagem)

            print(f'Mensagem enviada: {mensagem}')


    def enviar_logout(self):
        mensagem = self.email

        # Conectar ao RabbitMQ
        with pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672)) as connection:
            channel = connection.channel()

            # Publicar a mensagem na fila
            channel.basic_publish(exchange='', routing_key='fila_logout_passageiro', body=mensagem)

            print(f'Mensagem de logout enviada para o passageiro: {self.email}')
