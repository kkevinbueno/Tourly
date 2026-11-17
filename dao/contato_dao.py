
from routes.conexao import get_connection
from models.contato import Contato

class ContatoDAO:
    def salvar(self, contato):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contatos (nome, email, mensagem) VALUES (?, ?, ?)", (contato.nome, contato.email, contato.mensagem))
        conn.commit()
        conn.close()
