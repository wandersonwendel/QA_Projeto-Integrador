from model import User

def login_passageiro(email, senha):
    passageiro = User(email, senha)
    passageiro.enviar_login()


if __name__ == '__main__':
    login_passageiro('wandersonsousa489@gmail.com', 'lllksk')
