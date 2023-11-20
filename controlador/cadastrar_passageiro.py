from model import Passageiro

class ControladorCadastrarPassageiro:
    def __init__(self, banco_de_dados):
        self.banco_de_dados = banco_de_dados

    def cadastrar(self, nome, email, telefone, senha, endereco, sexo):
        passageiro = Passageiro(nome, email, telefone, senha, endereco, sexo)
        self.banco_de_dados.cadastrar_passageiro(passageiro)

