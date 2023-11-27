import psycopg2

class Mototaxi:
    def __init__(self, email, latitude, longitude, disponivel):
        self.email = email
        self.latitude = latitude
        self.longitude = longitude
        self.disponivel = disponivel

    @classmethod
    def verificar_existente(cls, email):
        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM mototaxis WHERE email=%s", (email,))
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count > 0

    def cadastrar(self):
        if self.verificar_existente(self.email):
            print(f"Um entregador com o e-mail {self.email} já está cadastrado.")
            

        conn = psycopg2.connect(database="itaxi", user="postgres", password="1234", host="localhost", port="5432")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO mototaxis (email, latitude, longitude, disponivel) VALUES (%s, %s, %s, %s)",
                       (self.email, self.latitude, self.longitude, self.disponivel))
        conn.commit()

        print(f"Entregador {self.email} cadastrado com sucesso!")

        cursor.close()
        conn.close()


mototaxi = Mototaxi('ari@gmail.com', 15, 1, True)
mototaxi.cadastrar()
