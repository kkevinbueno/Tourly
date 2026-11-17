from flask import Blueprint, request, jsonify
from dao.contato_dao import ContatoDAO
from models.contato import Contato

contato_bp = Blueprint("contato_bp", __name__)
dao = ContatoDAO()


def _campos_vazios(data, campos):
    return [c for c in campos if not str(data.get(c, "")).strip()]


@contato_bp.route("", methods=["POST"])
def salvar_contato():
    data = request.get_json(silent=True) or {}
    faltando = _campos_vazios(data, ["nome", "email", "mensagem"])
    if faltando:
        return jsonify({"error": "Campos obrigatórios: " + ", ".join(faltando)}), 400
    contato = Contato(data["nome"].strip(), data["email"].strip(), data["mensagem"].strip())
    dao.salvar(contato)
    return jsonify({"message": "Contato salvo com sucesso!", "contato": contato.to_dict()}), 201


@contato_bp.route("", methods=["GET"])
def listar_contatos():
    return jsonify([c.to_dict() for c in dao.listar_todos()]), 200
