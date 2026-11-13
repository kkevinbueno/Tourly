from flask import Blueprint, jsonify, request
from mysql.connector import Error

from dao.contato_dao import ContatoDAO
from models.contato import Contato

contato_bp = Blueprint("contato", __name__, url_prefix="/api/contatos")
dao = ContatoDAO()


def _erro(mensagem, status, detalhes=None):
    corpo = {"erro": mensagem}
    if detalhes:
        corpo["detalhes"] = detalhes
    return jsonify(corpo), status


def _ler_json():
    """Lê o corpo da requisição. Devolve None se não for um JSON válido (objeto)."""
    dados = request.get_json(silent=True)
    return dados if isinstance(dados, dict) else None


@contato_bp.errorhandler(Error)
def erro_banco(erro):
    print(f"[ERRO NO BANCO] {erro}")
    return _erro("Não foi possível acessar o banco de dados. Tente novamente mais tarde.", 500)


# READ — listar todos
@contato_bp.route("", methods=["GET"])
def listar():
    return jsonify([c.to_dict() for c in dao.listar()]), 200


# READ — buscar um
@contato_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    contato = dao.buscar_por_id(id)
    if contato is None:
        return _erro("Contato não encontrado.", 404)
    return jsonify(contato.to_dict()), 200


# CREATE
@contato_bp.route("", methods=["POST"])
def criar():
    dados = _ler_json()
    if dados is None:
        return _erro("Envie os dados em JSON (Content-Type: application/json).", 400)

    contato = Contato.from_dict(dados)
    erros = contato.validar()
    if erros:
        return _erro("Dados inválidos.", 400, erros)

    return jsonify(dao.inserir(contato).to_dict()), 201


# UPDATE
@contato_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    if dao.buscar_por_id(id) is None:
        return _erro("Contato não encontrado.", 404)

    dados = _ler_json()
    if dados is None:
        return _erro("Envie os dados em JSON (Content-Type: application/json).", 400)

    contato = Contato.from_dict(dados)
    contato.id = id
    erros = contato.validar()
    if erros:
        return _erro("Dados inválidos.", 400, erros)

    return jsonify(dao.atualizar(contato).to_dict()), 200


# DELETE
@contato_bp.route("/<int:id>", methods=["DELETE"])
def excluir(id):
    if not dao.excluir(id):
        return _erro("Contato não encontrado.", 404)
    return jsonify({"mensagem": "Contato excluído com sucesso."}), 200
