import pika

class MensagemCadastroVeiculo:
    def __init__(self, dados):
        self.dados = dados

    @property
    def placa(self):
        return self.dados['placa']

    @property
    def crlv(self):
        return self.dados['crlv']

    @property
    def fotoCNH(self):
        return self.dados['fotoCNH']

    @property
    def corVeiculo(self):
        return self.dados['corVeiculo']

    @property
    def modeloVeiculo(self):
        return self.dados['modeloVeiculo']

    @property
    def anoVeiculo(self):
        return self.dados['anoVeiculo']

    @property
    def renavam(self):
        return self.dados['renavam']

    @property
    def numeroChassi(self):
        return self.dados['numeroChassi']

    def enviar(self):
        # Conectar ao RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        channel = connection.channel()

        # Publicar a mensagem na fila
        channel.basic_publish(exchange='', routing_key='fila_cadastro_veiculo', body=self.to_string())

        print(f'Mensagem enviada: {self.to_string()}')

        connection.close()

    def to_string(self):
        return f"{self.placa};{self.crlv};{self.fotoCNH};{self.corVeiculo};{self.modeloVeiculo};{self.anoVeiculo};{self.renavam};{self.numeroChassi}"


dados = {
    'placa': 'abc123',
    'crlv': '(Documento)',
    'fotoCNH': '(Documento)',
    'corVeiculo': 'rosa',
    'modeloVeiculo': 'Peugeot',
    'anoVeiculo': '2020',
    'renavam': '12345678912',
    'numeroChassi': '99913493045421'
}

mensagem = MensagemCadastroVeiculo(dados)
mensagem.enviar()
