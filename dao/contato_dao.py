from routes.conexao import get_connection
from models.contato import Contato


class ContatoDAO:
    def salvar(self, contato):
        conn = get_connection()
        try:
            cur = conn.execute(
                "INSERT INTO contatos (nome, email, mensagem) VALUES (?, ?, ?)",
                (contato.nome, contato.email, contato.mensagem),
            )
            conn.commit()
            contato.id = cur.lastrowid
        finally:
            conn.close()
        return contato

    def listar_todos(self):
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM contatos ORDER BY id DESC").fetchall()
        finally:
            conn.close()
        return [Contato(r["nome"], r["email"], r["mensagem"], r["id"]) for r in rows]
