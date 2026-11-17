-- Banco de dados do Tourly (SQLite)
-- O arquivo banco.db é criado automaticamente na primeira execução do app.

CREATE TABLE IF NOT EXISTS contatos (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    nome     TEXT NOT NULL,
    email    TEXT NOT NULL,
    mensagem TEXT NOT NULL,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reservas (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    destino      TEXT NOT NULL,
    data_viagem  TEXT NOT NULL,
    nome_cliente TEXT NOT NULL,
    criado_em    TEXT DEFAULT CURRENT_TIMESTAMP
);
