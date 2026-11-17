
from flask import Blueprint, request, jsonify
from dao.reserva_dao import ReservaDAO
from models.reserva import Reserva

reserva_bp = Blueprint('reserva_bp', __name__)
dao = ReservaDAO()

@reserva_bp.route('', methods=['POST'])
def salvar_reserva():
    data = request.json
    reserva = Reserva(data['destino'], data['data_viagem'], data['nome_cliente'])
    dao.salvar(reserva)
    return jsonify({"message": "Reserva salva!"}), 201

@reserva_bp.route('', methods=['GET'])
def listar_reservas():
    reservas = dao.listar_todas()
    return jsonify([r.to_dict() for r in reservas]), 200

@reserva_bp.route('/<int:id>', methods=['DELETE'])
def excluir_reserva(id):
    dao.excluir(id)
    return jsonify({"message": "Reserva excluída!"}), 200
