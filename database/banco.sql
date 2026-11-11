-- ============================================================
-- Tourly — estrutura do banco de dados (MySQL 8)
-- Gerado a partir do diagrama de classes (docs/diagrama_classes.md)
-- ============================================================

CREATE DATABASE IF NOT EXISTS tourly
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE tourly;

-- ------------------------------------------------------------
-- usuario
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuario (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    nome           VARCHAR(100) NOT NULL,
    email          VARCHAR(150) NOT NULL UNIQUE,
    senha_hash     VARCHAR(255) NOT NULL,
    perfil         ENUM('turista', 'admin') NOT NULL DEFAULT 'turista',
    data_cadastro  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- destino
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS destino (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    cidade      VARCHAR(100) NOT NULL,
    estado      VARCHAR(50),
    pais        VARCHAR(60) NOT NULL DEFAULT 'Brasil',
    descricao   TEXT,
    imagem_url  VARCHAR(255)
);

-- ------------------------------------------------------------
-- ponto_turistico  (N pontos para 1 destino)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ponto_turistico (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    id_destino   INT NOT NULL,
    nome         VARCHAR(120) NOT NULL,
    categoria    VARCHAR(50),
    descricao    TEXT,
    endereco     VARCHAR(200),
    preco_medio  DECIMAL(10,2) DEFAULT 0.00,
    CONSTRAINT fk_ponto_destino
        FOREIGN KEY (id_destino) REFERENCES destino(id)
        ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- roteiro  (N roteiros para 1 usuário)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS roteiro (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario   INT NOT NULL,
    titulo       VARCHAR(120) NOT NULL,
    descricao    TEXT,
    data_inicio  DATE,
    data_fim     DATE,
    CONSTRAINT fk_roteiro_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id)
        ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- item_roteiro  (tabela associativa N:N roteiro <-> ponto_turistico)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS item_roteiro (
    id_roteiro  INT NOT NULL,
    id_ponto    INT NOT NULL,
    dia         INT NOT NULL DEFAULT 1,
    ordem       INT NOT NULL DEFAULT 1,
    horario     TIME,
    PRIMARY KEY (id_roteiro, id_ponto),
    CONSTRAINT fk_item_roteiro
        FOREIGN KEY (id_roteiro) REFERENCES roteiro(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_item_ponto
        FOREIGN KEY (id_ponto) REFERENCES ponto_turistico(id)
        ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- avaliacao  (usuário avalia ponto turístico, 1 avaliação por par)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS avaliacao (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario  INT NOT NULL,
    id_ponto    INT NOT NULL,
    nota        TINYINT NOT NULL,
    comentario  TEXT,
    data        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_avaliacao_nota CHECK (nota BETWEEN 1 AND 5),
    CONSTRAINT uq_avaliacao UNIQUE (id_usuario, id_ponto),
    CONSTRAINT fk_avaliacao_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuario(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_avaliacao_ponto
        FOREIGN KEY (id_ponto) REFERENCES ponto_turistico(id)
        ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- contato  (formulário de contato do site, sem relações)
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS contato (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL,
    mensagem    TEXT NOT NULL,
    data_envio  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);