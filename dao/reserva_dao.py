from routes.conexao import get_connection
from models.reserva import Reserva


class ReservaDAO:
    def salvar(self, reserva):
        conn = get_connection()
        try:
            cur = conn.execute(
                "INSERT INTO reservas (destino, data_viagem, nome_cliente) VALUES (?, ?, ?)",
                (reserva.destino, reserva.data_viagem, reserva.nome_cliente),
            )
            conn.commit()
            reserva.id = cur.lastrowid
        finally:
            conn.close()
        return reserva

    def listar_todas(self):
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM reservas ORDER BY data_viagem, id").fetchall()
        finally:
            conn.close()
        return [Reserva(r["destino"], r["data_viagem"], r["nome_cliente"], r["id"]) for r in rows]

    def excluir(self, id):
        conn = get_connection()
        try:
            cur = conn.execute("DELETE FROM reservas WHERE id = ?", (id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()

    def atualizar(self, reserva):
        conn = get_connection()
        try:
            cur = conn.execute(
                "UPDATE reservas SET destino = ?, data_viagem = ?, nome_cliente = ? WHERE id = ?",
                (reserva.destino, reserva.data_viagem, reserva.nome_cliente, reserva.id),
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()
