from conexao import Conexao
from models.contato import Contato


class ContatoDAO:
    """Acesso ao banco (SQL) da tabela `contato`. Nenhuma regra de tela fica aqui."""

    def __init__(self):
        self._conexao = Conexao()

    @staticmethod
    def _linha_para_contato(linha):
        return Contato(
            id=linha["id"],
            nome=linha["nome"],
            email=linha["email"],
            mensagem=linha["mensagem"],
            data_envio=linha["data_envio"],
        )

    def inserir(self, contato):
        """Grava um novo contato e devolve o objeto já com id e data_envio."""
        sql = "INSERT INTO contato (nome, email, mensagem) VALUES (%s, %s, %s)"
        con = self._conexao.conectar()
        try:
            cursor = con.cursor()
            cursor.execute(sql, (contato.nome, contato.email, contato.mensagem))
            con.commit()
            novo_id = cursor.lastrowid
            cursor.close()
        finally:
            con.close()
        return self.buscar_por_id(novo_id)

    def listar(self):
        """Devolve todos os contatos, do mais recente para o mais antigo."""
        sql = (
            "SELECT id, nome, email, mensagem, data_envio "
            "FROM contato ORDER BY data_envio DESC, id DESC"
        )
        con = self._conexao.conectar()
        try:
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql)
            linhas = cursor.fetchall()
            cursor.close()
        finally:
            con.close()
        return [self._linha_para_contato(linha) for linha in linhas]

    def buscar_por_id(self, id):
        """Devolve o contato com esse id, ou None se não existir."""
        sql = "SELECT id, nome, email, mensagem, data_envio FROM contato WHERE id = %s"
        con = self._conexao.conectar()
        try:
            cursor = con.cursor(dictionary=True)
            cursor.execute(sql, (id,))
            linha = cursor.fetchone()
            cursor.close()
        finally:
            con.close()
        return self._linha_para_contato(linha) if linha else None

    def atualizar(self, contato):
        """Atualiza nome, e-mail e mensagem do contato (identificado por contato.id)."""
        sql = "UPDATE contato SET nome = %s, email = %s, mensagem = %s WHERE id = %s"
        con = self._conexao.conectar()
        try:
            cursor = con.cursor()
            cursor.execute(sql, (contato.nome, contato.email, contato.mensagem, contato.id))
            con.commit()
            cursor.close()
        finally:
            con.close()
        return self.buscar_por_id(contato.id)

    def excluir(self, id):
        """Apaga o contato. Devolve True se apagou, False se o id não existia."""
        con = self._conexao.conectar()
        try:
            cursor = con.cursor()
            cursor.execute("DELETE FROM contato WHERE id = %s", (id,))
            con.commit()
            apagou = cursor.rowcount > 0
            cursor.close()
        finally:
            con.close()
        return apagou
