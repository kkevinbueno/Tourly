# Tourly

Projeto integrado de Desenvolvimento Web, Programação Orientada a Objetos e Banco de Dados.

## Requisitos
- Python 3.10 ou superior
- MySQL 8 ou compatível

## Configuração

1. Crie e ative um ambiente virtual:
   - Windows: `py -m venv .venv` e `.venv\\Scripts\\activate`
   - Linux/macOS: `python3 -m venv .venv` e `source .venv/bin/activate`
2. Instale as dependências: `pip install -r requirements.txt`.
3. Execute o script `database/banco.sql` no MySQL para criar o banco e as tabelas.
4. Configure as variáveis de ambiente, se necessário: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` e `DB_NAME`.
5. Inicie o site com `python app.py` e abra `http://127.0.0.1:5000`.

O formulário de contato envia JSON para `POST /api/contatos`. O endpoint `GET /api/health` informa se o servidor e o MySQL estão acessíveis.

## Observação
O front-end e a API são servidos pelo mesmo Flask, evitando problemas de CORS e garantindo que os caminhos `/api/...` funcionem localmente. A conexão com o banco só é exigida nas operações de contato e na verificação de saúde.
