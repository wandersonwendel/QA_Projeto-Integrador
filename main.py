import pika
from Model import VeiculoModel, CartaoModel, PassageiroModel, MototaxiModel, UsuarioModel
from View import PassageiroView, CartaoView, MototaxiView, UsuarioView
from Controller import VeiculoController, CartaoController, \
    PassageiroController,MototaxiController, UsuarioController



# Configurações do banco de dados
database_config = {
    'database': 'itaxi',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}

# Configurações do RabbitMQ
rabbitmq_config = {
    'host': 'localhost',
    'port': 5672
}

# Criar instâncias dos models
veiculo_model = VeiculoModel(database_config)
cartao_model = CartaoModel(database_config, rabbitmq_config)
passageiro_model = PassageiroModel(database_config)
mototaxi_model = MototaxiModel(database_config)
usuario_model = UsuarioModel(database_config)

# Criar instâncias das views
passageiro_view = PassageiroView()
cartao_view = CartaoView()
mototaxi_view = MototaxiView()
usuario_view = UsuarioView()

# Criar instâncias dos controllers
veiculo_controller = VeiculoController(veiculo_model)
cartao_controller = CartaoController(cartao_model, cartao_view)
passageiro_controller = PassageiroController(passageiro_model, passageiro_view)
mototaxi_controller = MototaxiController(mototaxi_model, mototaxi_view)
usuario_controller = UsuarioController(usuario_model, usuario_view)

# Testar algumas funcionalidades
veiculo_controller.cadastrar_veiculo('Carro', 'Ford', 'Fiesta', 2022, 'ABC1234')

passageiro_controller.atualizar_passageiro(1, 'mauricio', '8599999999')

mototaxi_controller.atualizar_mototaxi(1, 'poo Nelson', '999999999')

usuario_controller.realizar_login('123456789', 'senha123')

cartao_controller.cadastrar_cartao(1, 'Débito', '987654321')

usuario_controller.realizar_logout()