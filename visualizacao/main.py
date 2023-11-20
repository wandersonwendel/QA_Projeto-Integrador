from model import BancoDeDados
from controlador import ControladorCadastrarPassageiro

def main():
    banco_de_dados = BancoDeDados()
    controlador_cadastrar_passageiro = ControladorCadastrarPassageiro(banco_de_dados)

    while True:
        print("1 - Cadastrar passageiro")
        print("2 - Cadastrar mototaxi")
        print("3 - Login")
        print("4 - Logout")
        print("5 - Autorizar localização")
        print("6 - Cadastrar veículo")
        print("7 - Solicitar corrida")
        print("8 - Vincular cartão")
        print("9 - Desvincular cartão")
        print("0 - Sair")

        opcao = input("Opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("E-mail: ")
            telefone = input("Telefone: ")
            senha = input("Senha: ")
            endereco = input("Endereço: ")
            sexo = input("Sexo: ")

            controlador_cadastrar_passageiro.cadastrar(nome, email, telefone, senha, endereco, sexo)
        elif opcao == "2":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()