CREATE DATABASE itaxi;

\c itaxi;

-- cadastrar passageiro

CREATE TABLE passageiros (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    telefone VARCHAR(14),
    senha VARCHAR(255),
    endereco VARCHAR(20) NOT NULL,
    genero VARCHAR(20)
);

-- cadastrar veículo

CREATE TABLE veiculos (
    id SERIAL PRIMARY KEY,
    placa VARCHAR(8) UNIQUE NOT NULL,
    cor VARCHAR(30),
    modelo VARCHAR(255) NOT NULL,
    ano INTEGER NOT NULL,
    renavam VARCHAR(12) NOT NULL,
    chassi VARCHAR(18) NOT NULL
);

-- cadastrar mototaxi

CREATE TABLE mototaxis (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    telefone VARCHAR(14),
    genero VARCHAR(20),
    senha VARCHAR(255) NOT NULL,
    crlv VARCHAR(12) NOT NULL,
    cnh VARCHAR(9) NOT NULL,
    disponibilidade BOOLEAN,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
);

-- tabela corridas

CREATE TABLE corridas (
    id SERIAL PRIMARY KEY,
    passageiro_id INTEGER NOT NULL,
    endereco_destino VARCHAR(255) NOT NULL,
    mototaxi_id INTEGER,
    status VARCHAR(50),
    FOREIGN KEY (passageiro_id) REFERENCES passageiros(id),
    FOREIGN KEY (mototaxi_id) REFERENCES mototaxis(id)
);


CREATE TABLE cartoes (
    id SERIAL PRIMARY KEY,
    passageiro_id INTEGER,
    titular VARCHAR(255) NOT NULL,
    cvv INTEGER(3),
    validade VARCHAR(10),
    tipo VARCHAR(10),
    numero VARCHAR(16),
    CONSTRAINT fk_passageiro FOREIGN KEY (passageiro_id)
        REFERENCES passageiros(id)
);