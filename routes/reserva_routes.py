from datetime import date
from flask import Blueprint, request, jsonify
from dao.reserva_dao import ReservaDAO
from models.reserva import Reserva

reserva_bp = Blueprint("reserva_bp", __name__)
dao = ReservaDAO()


def _validar(data):
    faltando = [c for c in ("destino", "data_viagem", "nome_cliente") if not str(data.get(c, "")).strip()]
    if faltando:
        return "Campos obrigatórios: " + ", ".join(faltando)
    try:
        date.fromisoformat(data["data_viagem"])
    except ValueError:
        return "data_viagem deve estar no formato AAAA-MM-DD"
    return None


@reserva_bp.route("", methods=["POST"])
def salvar_reserva():
    data = request.get_json(silent=True) or {}
    erro = _validar(data)
    if erro:
        return jsonify({"error": erro}), 400
    reserva = Reserva(data["destino"].strip(), data["data_viagem"], data["nome_cliente"].strip())
    dao.salvar(reserva)
    return jsonify({"message": "Reserva salva!", "reserva": reserva.to_dict()}), 201


@reserva_bp.route("", methods=["GET"])
def listar_reservas():
    return jsonify([r.to_dict() for r in dao.listar_todas()]), 200


@reserva_bp.route("/<int:id>", methods=["DELETE"])
def excluir_reserva(id):
    if not dao.excluir(id):
        return jsonify({"error": "Reserva não encontrada"}), 404
    return jsonify({"message": "Reserva excluída!"}), 200


@reserva_bp.route("/<int:id>", methods=["PUT"])
def atualizar_reserva(id):
    data = request.get_json(silent=True) or {}
    erro = _validar(data)
    if erro:
        return jsonify({"error": erro}), 400
    reserva = Reserva(data["destino"].strip(), data["data_viagem"], data["nome_cliente"].strip(), id)
    if not dao.atualizar(reserva):
        return jsonify({"error": "Reserva não encontrada"}), 404
    return jsonify({"message": "Reserva atualizada!", "reserva": reserva.to_dict()}), 200
