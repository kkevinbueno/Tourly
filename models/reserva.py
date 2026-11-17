
class Reserva:
    def __init__(self, destino, data_viagem, nome_cliente, id=None):
        self.id = id
        self.destino = destino
        self.data_viagem = data_viagem
        self.nome_cliente = nome_cliente

    def to_dict(self):
        return {"id": self.id, "destino": self.destino, "data_viagem": self.data_viagem, "nome_cliente": self.nome_cliente}
