from model import User

   

def logout_passageiro(email):
    passageiro = User(email)
    passageiro.enviar_logout()


if __name__ == '__main__':
    logout_passageiro('wandersonsousa489@gmail.com')
