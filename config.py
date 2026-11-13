import os


class Config:
    """Configurações do sistema. Para mudar algo, altere aqui (ou use variáveis de ambiente)."""

    # --- Banco de dados (MySQL) ---
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "tourly")

    # --- Servidor Flask ---
    FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    DEBUG = True
