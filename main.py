import pika
from Model.models import VeiculoModel, CartaoModel, PassageiroModel, MototaxiModel, UsuarioModel
from View.views import PassageiroView, CartaoView, MototaxiView, UsuarioView
from Controller.controllers import VeiculoController, CartaoController, \
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
veiculo_controller.cadastrar_veiculo('abc123', 'preto', 'Fiesta', 2022, 'ABC1234', '000000')

passageiro_controller.cadastrar_passageiro('wan', 'wand@gmail.com', '93829472', 'jsfdsfg', 'masc', 'dhsjffg')

mototaxi_controller.cadastrar_mototaxi('wan', 'wand@gmail.com', '93829472', 'masc', '48385685', '4748566', '921382', True, 5.6487, 10.3535)

usuario_controller.realizar_login('wand@gmail.com', 'jsfdsfg')

cartao_controller.cadastrar_cartao(1, 'Wan W S Lopes', '321', '2030', 'débito', '927497233')

usuario_controller.realizar_logout()