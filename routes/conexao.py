import mysql.connector
from routes.config import Config


class Conexao:
    """Abre conexões com o MySQL usando as configurações do projeto."""
    def __init__(self):
        self._parametros = {
            "host": Config.DB_HOST,
            "port": Config.DB_PORT,
            "user": Config.DB_USER,
            "password": Config.DB_PASSWORD,
            "database": Config.DB_NAME,
            "charset": "utf8mb4",
            "connection_timeout": 5,
        }

    def conectar(self):
        return mysql.connector.connect(**self._parametros)
