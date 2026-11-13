import re
from datetime import datetime


class Contato:
    """Representa uma mensagem enviada pelo formulário de contato (tabela `contato`)."""

    _REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, nome, email, mensagem, id=None, data_envio=None):
        self.id = id
        self.nome = self._texto(nome)
        self.email = self._texto(email)
        self.mensagem = self._texto(mensagem)
        self.data_envio = data_envio

    @staticmethod
    def _texto(valor):
        """Converte para texto sem espaços nas pontas (None vira texto vazio)."""
        return "" if valor is None else str(valor).strip()

    def validar(self):
        """Devolve uma lista com as mensagens de erro. Lista vazia = dados válidos."""
        erros = []

        if not self.nome:
            erros.append("O nome é obrigatório.")
        elif len(self.nome) > 100:
            erros.append("O nome deve ter no máximo 100 caracteres.")

        if not self.email:
            erros.append("O e-mail é obrigatório.")
        elif len(self.email) > 150:
            erros.append("O e-mail deve ter no máximo 150 caracteres.")
        elif not self._REGEX_EMAIL.match(self.email):
            erros.append("O e-mail informado não é válido.")

        if not self.mensagem:
            erros.append("A mensagem é obrigatória.")

        return erros

    def to_dict(self):
        """Converte o objeto em dicionário, pronto para virar JSON."""
        data = self.data_envio
        if isinstance(data, datetime):
            data = data.isoformat(sep=" ")
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "mensagem": self.mensagem,
            "data_envio": data,
        }

    @classmethod
    def from_dict(cls, dados):
        """Cria um Contato a partir do JSON recebido do front-end."""
        return cls(
            nome=dados.get("nome"),
            email=dados.get("email"),
            mensagem=dados.get("mensagem"),
        )
