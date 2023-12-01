""" O módulo psycopg2 é responsável por conectar o código com o banco de dados
    O módulo pika é responsável por fazer a conexão do servidor com o rabbitMQ """
import psycopg2
import pika


class VeiculoModel:
    def _init_(self, database_config, rabbitmq_config):
        self.database_config = database_config
        self.rabbitmq_config = rabbitmq_config

    def cadastrar_veiculo(self, placa, cor, modelo, ano, renavam, chassi):
        try:
            with psycopg2.connect(**self.database_config) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO veiculos (placa, cor, modelo, ano, renavam, chassi) VALUES (%s, %s, %s, %s, %s, %s)",
                               (placa, cor, modelo, ano, renavam, chassi))
                conn.commit()
                self.enviar_mensagem(placa, cor, modelo, ano, renavam, chassi)
                return True
        except psycopg2.Error as e:
            print(f"Ocorreu um erro ao acessar o banco de dados: {e}")
            return False

    def enviar_mensagem(self, placa, cor, modelo, ano, renavam, chassi):
        mensagem = f"{placa};{cor};{modelo};{ano};{renavam};{chassi}"
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(**self.rabbitmq_config))
            channel = connection.channel()
            channel.basic_publish(exchange='', routing_key='fila_veiculos', body=mensagem)
            print(f'Mensagem enviada: {mensagem}')
            connection.close()
        except pika.exceptions.AMQPError as amqp_error:
            print(f"Erro no RabbitMQ ao enviar mensagem: {amqp_error}")

class CartaoModel:
    """ Classe referente ao modelo cartão """
    def _init_(self, database_config, rabbitmq_config):
        self.database_config = database_config
        self.rabbitmq_config = rabbitmq_config

    def conectar_banco(self):
        """ Método responsável por fazer a conexão do servidor com banco de dados """
        return psycopg2.connect(**self.database_config)

    def cadastrar_cartao(self, passageiro_id, titular, cvv, validade, tipo, numero):
        """ Método responsável por inserir o cartão no banco de dados """
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO cartoes (passageiro_id, titular, cvv, validade, tipo, numero) VALUES (%s, %s, %s, %s, %s, %s)",
            (passageiro_id, titular, cvv, validade, tipo, numero))
            conn.commit()
            return True
        except psycopg2.IntegrityError as integrity_error:
            # Lidar com violação de integridade (por exemplo, chave única)
            print(f"Erro de integridade ao cadastrar cartão: {integrity_error}")
            return False

        except psycopg2.DataError as data_error:
            # Lidar com erros de dados (por exemplo, tipo de dados incorreto)
            print(f"Erro de dados ao cadastrar cartão: {data_error}")
            return False

        except psycopg2.DatabaseError as db_error:
            # Lidar com outros erros relacionados ao banco de dados
            print(f"Erro de banco de dados ao cadastrar cartão: {db_error}")
            return False
        finally:
            cursor.close()
            conn.close()

    def desvincular_cartao(self, passageiro_id, titular, numero):
        """ Método responsável por desvincular o cartão no banco de dados """
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("DELETE FROM cartoes WHERE passageiro_id=%s AND titular=%s AND numero=%s", (passageiro_id, titular, numero))
            conn.commit()
            return True
        except psycopg2.IntegrityError as integrity_error:
            # Lidar com violação de integridade (por exemplo, chave única)
            print(f"Erro de integridade ao desvincular cartão: {integrity_error}")
            return False

        except psycopg2.DataError as data_error:
            # Lidar com erros de dados (por exemplo, tipo de dados incorreto)
            print(f"Erro de dados ao desvincular cartão: {data_error}")
            return False

        except psycopg2.DatabaseError as db_error:
            # Lidar com outros erros relacionados ao banco de dados
            print(f"Erro de banco de dados ao desvincular cartão: {db_error}")
            return False
        finally:
            cursor.close()
            conn.close()

    def enviar_resposta_para_passageiro(self, passageiro_id, mensagem):
        """ Método responsável por dar o retorno da requisição do cliente """
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(**self.rabbitmq_config))
            channel = connection.channel()

            channel.queue_declare(queue=f'fila_respostas_{passageiro_id}')
            channel.basic_publish(exchange='', routing_key=f'fila_respostas_{passageiro_id}',
            body=mensagem)

            print(f'Mensagem enviada para o passageiro {passageiro_id}: {mensagem}')

            connection.close()

        except pika.exceptions.AMQPError as amqp_error:
            # Lidar com erros específicos do RabbitMQ
            print(f"Erro no RabbitMQ ao enviar mensagem para o passageiro {passageiro_id}: {amqp_error}")

class PassageiroModel:
    """ Classe referente ao modelo Passageiro """
    def _init_(self, database_config):
        self.database_config = database_config

    def conectar_banco(self):
        """ Método responsável por conectar com o banco de dados """
        return psycopg2.connect(**self.database_config)
    
    def cadastrar_passageiro(self, nome, email, telefone, senha, endereco, genero):
        """ Método responsável por cadastrar os dados do cliente """
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO passageiros (nome, email, telefone, senha, endereco, genero) VALUES (%s, %s, %s, %s, %s, %s)",
                           (nome, email, telefone, senha, endereco, genero))
            conn.commit()
        except psycopg2.IntegrityError as integrity_error:
            # Lidar com violação de integridade (por exemplo, chave única)
            print(f"Erro de integridade ao cadastrar dados do passageiro: {integrity_error}")
            conn.rollback()
        except psycopg2.DataError as data_error:
            # Lidar com erros de dados (por exemplo, tipo de dados incorreto)
            print(f"Erro de dados ao cadastrar dados do passageiro: {data_error}")
            conn.rollback()
        except psycopg2.DatabaseError as db_error:
            # Lidar com outros erros relacionados ao banco de dados
            print(f"Erro de banco de dados ao cadastrar dados do passageiro: {db_error}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def atualizar_cliente(self, passageiro_id, novo_nome, novo_telefone):
        """ Método responsável por atualizar os dados do cliente """
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE clientes SET nome = %s, telefone = %s WHERE id = %s",
                           (novo_nome, novo_telefone, passageiro_id))
            conn.commit()
            print(f'Dados do Cliente {passageiro_id} atualizados com sucesso.')
        except psycopg2.IntegrityError as integrity_error:
            # Lidar com violação de integridade (por exemplo, chave única)
            print(f"Erro de integridade ao atualizar dados do cliente: {integrity_error}")
            conn.rollback()
        except psycopg2.DataError as data_error:
            # Lidar com erros de dados (por exemplo, tipo de dados incorreto)
            print(f"Erro de dados ao atualizar dados do cliente: {data_error}")
            conn.rollback()
        except psycopg2.DatabaseError as db_error:
            # Lidar com outros erros relacionados ao banco de dados
            print(f"Erro de banco de dados ao atualizar dados do cliente: {db_error}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

class MototaxiModel:
    """ Classe responsável pelo modelo do entregador """
    def _init_(self, database_config):
        self.database_config = database_config

    def conectar_banco(self):
        """ Responsável por conectar com o banco de dados """
        return psycopg2.connect(**self.database_config)
    
    def cadastrar_mototaxi(self, nome, email, telefone, genero, senha, crlv, cnh, disponibilidade, latitude, longitude):
        """ Método responsável por cadastrar os dados do cliente """
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO mototaxis (nome, email, telefone, genero, senha, crlv, cnh, disponibilidade, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (nome, email, telefone, genero, senha, crlv, cnh, disponibilidade, latitude, longitude))
            conn.commit()
        except psycopg2.IntegrityError as integrity_error:
            # Lidar com violação de integridade (por exemplo, chave única)
            print(f"Erro de integridade ao cadastrar dados do mototaxi: {integrity_error}")
            conn.rollback()
        except psycopg2.DataError as data_error:
            # Lidar com erros de dados (por exemplo, tipo de dados incorreto)
            print(f"Erro de dados ao cadastrar dados do mototaxi: {data_error}")
            conn.rollback()
        except psycopg2.DatabaseError as db_error:
            # Lidar com outros erros relacionados ao banco de dados
            print(f"Erro de banco de dados ao cadastrar dados do mototaxi: {db_error}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def atualizar_mototaxi(self, mototaxi_id, novo_nome, novo_telefone):
        """ Método responsável por atualizar os dados do mototaxi """
        conn = self.conectar_banco()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE mototaxis SET nome = %s, telefone = %s WHERE id = %s",
                           (novo_nome, novo_telefone, mototaxi_id))
            conn.commit()
            print(f'Dados do Mototaxi {mototaxi_id} atualizados com sucesso.')
        except psycopg2.IntegrityError as integrity_error:
            # Lidar com violação de integridade (por exemplo, chave única)
            print(f"Erro de integridade ao atualizar dados do mototaxi: {integrity_error}")
            conn.rollback()
        except psycopg2.DataError as data_error:
            # Lidar com erros de dados (por exemplo, tipo de dados incorreto)
            print(f"Erro de dados ao atualizar dados do mototaxi: {data_error}")
            conn.rollback()
        except psycopg2.DatabaseError as db_error:
            # Lidar com outros erros relacionados ao banco de dados
            print(f"Erro de banco de dados ao atualizar dados do mototaxi: {db_error}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

class UsuarioModel:
    """ Classe referente ao modelo usuario """
    def _init_(self, database_config):
        self.database_config = database_config

    def fazer_login(self, email, senha):
        """ Metodo responsavel por fazer login """
        try:
            with psycopg2.connect(**self.database_config) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM passageiros WHERE email=%s AND senha=%s", (email, senha))
                usuario = cursor.fetchone()
                return usuario[1] if usuario else None  # Retorna o nome do usuário

        except psycopg2.Error as e:
            print(f"Ocorreu um erro ao acessar o banco de dados: {e}")
            return None

    def fazer_logout(self):
        """ Metodo para fazer logout """
        return True
