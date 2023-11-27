import pika

class MensagemCadastroUsuario:
    def __init__(self, nome, email, telefone, senha, endereco, sexo):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.endereco = endereco
        self.sexo = sexo

    def enviar(self):
        # Conectar ao RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()

        # Publicar a mensagem na fila
        channel.basic_publish(exchange='', routing_key='fila_cadastrar_passageiro', body=self.to_string())

        print(f'Mensagem enviada: {self.to_string()}')

        connection.close()

    def to_string(self):
        return f"{self.nome};{self.email};{self.telefone};{self.senha};{self.endereco};{self.sexo}"


mensagem = MensagemCadastroUsuario('Wanderson', 'wandersonsousa489@gmail.com', '00972844', 'lllksk', 'ksdhjfuigud', 'senha123')
mensagem.enviar()


