# Diagrama de classes — Tourly

```mermaid
classDiagram
    class Contato {
        +int id
        +str nome
        +str email
        +str mensagem
        +datetime data_envio
        +validar() list
        +to_dict() dict
        +from_dict(dados) Contato
    }
    class ContatoDAO {
        -Conexao _conexao
        +inserir(contato) Contato
        +listar() list
        +buscar_por_id(id) Contato
        +atualizar(contato) Contato
        +excluir(id) bool
    }
    class Conexao {
        -dict _parametros
        +conectar()
    }
    ContatoDAO --> Conexao
    ContatoDAO --> Contato
```

A camada `routes/contato_routes.py` recebe as requisições HTTP, valida os dados por meio de `Contato` e delega a persistência ao `ContatoDAO`. `Conexao` centraliza a abertura das conexões MySQL.
