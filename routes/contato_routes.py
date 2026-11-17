
from flask import Blueprint, request, jsonify
from dao.contato_dao import ContatoDAO
from models.contato import Contato

contato_bp = Blueprint('contato_bp', __name__)
dao = ContatoDAO()

@contato_bp.route('', methods=['POST'])
def salvar_contato():
    data = request.json
    contato = Contato(data['nome'], data['email'], data['mensagem'])
    dao.salvar(contato)
    return jsonify({"message": "Contato salvo com sucesso!"}), 201
