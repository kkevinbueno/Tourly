
from routes.conexao import get_connection
from models.reserva import Reserva

class ReservaDAO:
    def salvar(self, reserva):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reservas (destino, data_viagem, nome_cliente) VALUES (?, ?, ?)", 
                       (reserva.destino, reserva.data_viagem, reserva.nome_cliente))
        conn.commit()
        conn.close()

    def listar_todas(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservas")
        rows = cursor.fetchall()
        conn.close()
        return [Reserva(row['destino'], row['data_viagem'], row['nome_cliente'], row['id']) for row in rows]

    def excluir(self, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reservas WHERE id = ?", (id,))
        conn.commit()
        conn.close()
