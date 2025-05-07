DROP TABLE IF EXISTS visitantes_eventos;
DROP TABLE IF EXISTS visitantes_apartamento;
DROP TABLE IF EXISTS agendamento_evento;
DROP TABLE IF EXISTS moradores;

CREATE TABLE moradores (
    cpf INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    apartamento TEXT NOT NULL,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE agendamento_evento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpf_morador INTEGER NOT NULL,
    data DATE NOT NULL,
    local INTEGER NOT NULL,
    ambientes TEXT NOT NULL CHECK (ambientes IN ('churrasqueira', 'salão de festas')),
    apartamento TEXT NOT NULL,
    FOREIGN KEY (cpf_morador) REFERENCES moradores(cpf)
);

CREATE TABLE visitantes_apartamento (
    cpf_visitante INTEGER PRIMARY KEY,
    cpf_morador INTEGER NOT NULL,
    nome TEXT,
    apartamento TEXT,
    FOREIGN KEY (cpf_morador) REFERENCES moradores(cpf)
);

CREATE TABLE visitantes_eventos (
    cpf_visitante INTEGER PRIMARY KEY,
    cpf_morador INTEGER NOT NULL,
    nome TEXT,
    apartamento TEXT,
    FOREIGN KEY (cpf_morador) REFERENCES moradores(cpf)
);

-- Dados de exemplo para moradores
INSERT INTO moradores (cpf, nome, apartamento, email, senha) VALUES
(26556898741, 'Gabriel', '101', 'emailGabriel@email.com', '1111'),
(28835445881, 'Fabiana', '102', 'emailFabiana@email.com', '2222');
