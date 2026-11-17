import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "banco.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "banco.sql")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria as tabelas a partir de database/banco.sql."""
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        script = f.read()
    conn = get_connection()
    conn.executescript(script)
    conn.commit()
    conn.close()


init_db()
