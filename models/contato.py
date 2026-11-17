
class Contato:
    def __init__(self, nome, email, mensagem, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.mensagem = mensagem
    
    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "email": self.email, "mensagem": self.mensagem}
