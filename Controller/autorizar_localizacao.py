import pika

class SolicitacaoAutorizacao:
    def __init__(self, email, aceita_permissao):
        self.email = email
        self.aceita_permissao = aceita_permissao

    def enviar(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()

        mensagem = f"{self.email};{self.aceita_permissao}"

        channel.basic_publish(exchange='', routing_key='fila_autorizar_localizacao', body=mensagem)

        print(f"Mensagem enviada: {mensagem}")

        connection.close()


solicitacao = SolicitacaoAutorizacao('wandersonsousa489@gmail.com', 'sim')
solicitacao.enviar()
