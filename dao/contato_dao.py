from routes.conexao import Conexao
from models.contato import Contato


class ContatoDAO:
    """Operações de persistência da entidade Contato."""
    def __init__(self):
        self._conexao = Conexao()

    @staticmethod
    def _linha_para_contato(linha):
        return Contato(id=linha["id"], nome=linha["nome"], email=linha["email"],
                       mensagem=linha["mensagem"], data_envio=linha["data_envio"])

    def inserir(self, contato):
        con = self._conexao.conectar()
        try:
            cursor = con.cursor()
            cursor.execute("INSERT INTO contato (nome, email, mensagem) VALUES (%s, %s, %s)",
                           (contato.nome, contato.email, contato.mensagem))
            con.commit()
            novo_id = cursor.lastrowid
            cursor.close()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()
        return self.buscar_por_id(novo_id)

    def listar(self):
        con = self._conexao.conectar()
        try:
            cursor = con.cursor(dictionary=True)
            cursor.execute("SELECT id, nome, email, mensagem, data_envio FROM contato ORDER BY data_envio DESC, id DESC")
            linhas = cursor.fetchall()
            cursor.close()
            return [self._linha_para_contato(linha) for linha in linhas]
        finally:
            con.close()

    def buscar_por_id(self, contato_id):
        con = self._conexao.conectar()
        try:
            cursor = con.cursor(dictionary=True)
            cursor.execute("SELECT id, nome, email, mensagem, data_envio FROM contato WHERE id = %s", (contato_id,))
            linha = cursor.fetchone()
            cursor.close()
            return self._linha_para_contato(linha) if linha else None
        finally:
            con.close()

    def atualizar(self, contato):
        con = self._conexao.conectar()
        try:
            cursor = con.cursor()
            cursor.execute("UPDATE contato SET nome=%s, email=%s, mensagem=%s WHERE id=%s",
                           (contato.nome, contato.email, contato.mensagem, contato.id))
            con.commit()
            cursor.close()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()
        return self.buscar_por_id(contato.id)

    def excluir(self, contato_id):
        con = self._conexao.conectar()
        try:
            cursor = con.cursor()
            cursor.execute("DELETE FROM contato WHERE id = %s", (contato_id,))
            con.commit()
            apagou = cursor.rowcount > 0
            cursor.close()
            return apagou
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()
