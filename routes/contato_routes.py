from flask import Blueprint, jsonify, request
from mysql.connector import Error
from dao.contato_dao import ContatoDAO
from models.contato import Contato

contato_bp = Blueprint("contato", __name__, url_prefix="/api/contatos")
dao = ContatoDAO()


def erro(mensagem, status, detalhes=None):
    resposta = {"erro": mensagem}
    if detalhes:
        resposta["detalhes"] = detalhes
    return jsonify(resposta), status


@contato_bp.errorhandler(Error)
def erro_banco(exc):
    print(f"[ERRO NO BANCO] {exc}")
    return erro("Não foi possível acessar o banco de dados. Confira a configuração e tente novamente.", 503)


@contato_bp.get("")
def listar():
    return jsonify([contato.to_dict() for contato in dao.listar()])


@contato_bp.get("/<int:contato_id>")
def buscar(contato_id):
    contato = dao.buscar_por_id(contato_id)
    return (jsonify(contato.to_dict()), 200) if contato else erro("Contato não encontrado.", 404)


@contato_bp.post("")
def criar():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return erro("Envie os campos em JSON.", 400)
    contato = Contato.from_dict(dados)
    erros = contato.validar()
    if erros:
        return erro("Confira os dados informados.", 400, erros)
    return jsonify(dao.inserir(contato).to_dict()), 201


@contato_bp.put("/<int:contato_id>")
def atualizar(contato_id):
    if dao.buscar_por_id(contato_id) is None:
        return erro("Contato não encontrado.", 404)
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return erro("Envie os campos em JSON.", 400)
    contato = Contato.from_dict(dados)
    contato.id = contato_id
    erros = contato.validar()
    if erros:
        return erro("Confira os dados informados.", 400, erros)
    return jsonify(dao.atualizar(contato).to_dict())


@contato_bp.delete("/<int:contato_id>")
def excluir(contato_id):
    if not dao.excluir(contato_id):
        return erro("Contato não encontrado.", 404)
    return jsonify({"mensagem": "Contato excluído com sucesso."})
