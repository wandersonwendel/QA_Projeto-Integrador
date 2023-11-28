""" Módulo pika é responsável por fazer a conexão entre rabbitMQ e o servidor """
import pika

class VeiculoController:
    """ Classe responsável pelo modelo Veículo """
    def __init__(self, model):
        self.model = model

    def cadastrar_veiculo(self, placa, cor, modelo, ano, renavam, chassi):
        """ Método responsável por fazer a inserção do veiculo no banco de dados """
        sucesso = self.model.cadastrar_veiculo(placa, cor, modelo, ano, renavam, chassi)
        if sucesso:
            self.enviar_mensagem(placa, cor, modelo, ano, renavam, chassi)

    def enviar_mensagem(self, placa, cor, modelo, ano, renavam, chassi):
        """ Método responsável por enviar mensagem para o rabbitMQ """
        mensagem = f"{placa};{cor};{modelo};{ano};{renavam};{chassi}"
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
            port=5672))
            channel = connection.channel()
            channel.basic_publish(exchange='', routing_key='fila_veiculos', body=mensagem)
            print(f'Mensagem enviada: {mensagem}')
            connection.close()
        except pika.exceptions.AMQPError as amqp_error:
            # Lidar com erros específicos do RabbitMQ
            print(f"Erro no RabbitMQ ao enviar mensagem: {amqp_error}")

class CartaoController:
    """ Classe responsável pelo controle do Cartão """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def cadastrar_cartao(self, passageiro_id, titular, cvv, validade, tipo, numero):
        """ Método responsável por inserir o cartão no banco de dados """
        if self.model.cadastrar_cartao(passageiro_id, titular, cvv, validade, tipo, numero):
            self.view.mostrar_mensagem("Cartão cadastrado com sucesso!")
            self.model.enviar_resposta_para_passageiro(passageiro_id, "RESPOSTA_CADASTRO_CARTAO; SUCESSO")
        else:
            self.view.mostrar_mensagem("Erro ao cadastrar o cartão.")
            self.model.enviar_resposta_para_passageiro(passageiro_id, "RESPOSTA_CADASTRO_CARTAO; ERRO")

    def desvincular_cartao(self, passageiro_id, titular, numero):
        """ Método responsável por desvincular o cartão no banco de dados """
        if self.model.desvincular_cartao(passageiro_id, titular,numero):
            self.view.mostrar_mensagem("Cartão desvinculado com sucesso!")
            self.model.enviar_resposta_para_passageiro(passageiro_id, "RESPOSTA_DESVINCULAR_CARTAO; SUCESSO")
        else:
            self.view.mostrar_mensagem("Erro ao desvincular o cartão.")
            self.model.enviar_resposta_para_passageiro(passageiro_id, "RESPOSTA_DESVINCULAR_CARTAO; ERRO")

class PassageiroController:
    """ Método responsável pelo controle do cliente """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def cadastrar_passageiro(self, nome, email, telefone, senha, endereco, genero):
         """ Médodo responsável por cadastrar os dados do passageiro """
         self.model.cadastrar_passageiro(nome, email, telefone, senha, endereco, genero)
         mensagem = f'Passageiro {nome} cadastrado com sucesso.'
         self.view.mostrar_mensagem(mensagem)

    def atualizar_passageiro(self, passageiro_id, novo_nome, novo_telefone):
        """ Médodo responsável por atualizar os dados do cliente """
        self.model.atualizar_passageiro(passageiro_id, novo_nome, novo_telefone)
        mensagem = f'Dados do Cliente {passageiro_id} atualizados com sucesso.'
        self.view.mostrar_mensagem(mensagem)


class MototaxiController:
    """ Classe responsável pelo controle do Entregador """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def cadastrar_mototaxi(self, nome, email, telefone, genero, senha, crlv, cnh, disponibilidade, latitude, longitude):
         """ Médodo responsável por cadastrar os dados do mototaxi """
         self.model.cadastrar_mototaxi(nome, email, telefone, genero, senha, crlv, cnh, disponibilidade, latitude, longitude)
         mensagem = f'Mototaxi {nome} cadastrado com sucesso.'
         self.view.mostrar_mensagem(mensagem)

    def atualizar_mototaxi(self, mototaxi_id, novo_nome, novo_telefone):
        """ Método responsável por atualizar os dados do mototaxi """
        self.model.atualizar_mototaxi(mototaxi_id, novo_nome, novo_telefone)
        mensagem = f'Dados do mototaxi {mototaxi_id} atualizados com sucesso.'
        self.view.mostrar_mensagem(mensagem)

class UsuarioController:
    """ Classe responsável pelo controle do usuario """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def realizar_login(self, email, senha):
        """ Método responsável pelo controle do login de usuário """
        nome_usuario = self.model.fazer_login(email, senha)
        if nome_usuario:
            self.view.mostrar_mensagem(f"Bem-vindo, {nome_usuario}!")

    def realizar_logout(self):
        """ Método responsável pelo controle do logout de usuário """
        sucesso = self.model.fazer_logout()
        if sucesso:
            self.view.mostrar_mensagem("Logout bem-sucedido!")
        else:
            self.view.mostrar_mensagem("Falha ao fazer logout.")

    def excluir_conta(self, email, senha):
        """ Método responsável pela exclusão de conta do usuário """
        if self.model.verificar_credenciais(email, senha):  # Assumindo que há um método para verificar as credenciais
            confirmacao = input("Tem certeza de que deseja excluir sua conta? (Digite 'sim' para confirmar): ")
            if confirmacao.lower() == 'sim':
                self.model.excluir_conta(email)  # Assumindo que há um método para excluir a conta no modelo
                self.view.mostrar_mensagem("Sua conta foi excluída com sucesso.")
            else:
                self.view.mostrar_mensagem("Exclusão de conta cancelada.")
        else:
            self.view.mostrar_mensagem("Credenciais inválidas. Não é possível excluir a conta.")
