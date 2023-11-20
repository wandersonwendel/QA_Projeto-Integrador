class Passageiro:
    def __init__(self, nome, email, telefone, senha, endereco, sexo):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha
        self.endereco = endereco
        self.sexo = sexo

    def cadastrar(self, banco_de_dados):
        with banco_de_dados.cursor() as cursor:
            cursor.execute("INSERT INTO passageiros (nome, email, telefone, senha, endereco, sexo) VALUES (%s, %s, %s, %s, %s, %s)",
                           (self.nome, self.email, self.telefone, self.senha, self.endereco, self.sexo))
        banco_de_dados.commit()
