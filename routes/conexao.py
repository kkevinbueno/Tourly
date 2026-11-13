import mysql.connector

from config import Config


class Conexao:
    """Responsável apenas por abrir a conexão com o banco de dados."""

    def __init__(self):
        self._parametros = {
            "host": Config.DB_HOST,
            "port": Config.DB_PORT,
            "user": Config.DB_USER,
            "password": Config.DB_PASSWORD,
            "database": Config.DB_NAME,
            "charset": "utf8mb4",
        }

    def conectar(self):
        """Abre e devolve uma nova conexão. Quem chama deve fechá-la (con.close())."""
        return mysql.connector.connect(**self._parametros)
