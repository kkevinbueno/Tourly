
import sqlite3
def get_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn
    
def init_db():
    conn = get_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS reservas (id INTEGER PRIMARY KEY AUTOINCREMENT, destino TEXT, data_viagem TEXT, nome_cliente TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS contatos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, email TEXT, mensagem TEXT)''')
    conn.commit()
    conn.close()

init_db()
