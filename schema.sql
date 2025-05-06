DROP TABLE IF EXISTS moradores;
DROP TABLE IF EXISTS agendamento_evento;
DROP TABLE IF EXISTS visitantes_apartamento;
DROP TABLE IF EXISTS visitantes_eventos;

CREATE TABLE moradores (
    cpf INT PRIMARY KEY, --Natural Key (NK) para cada morador, remove uma coluna (id), visando otimizar armazenamento
    nome VARCHAR(50) NOT NULL,
    apartamento VARCHAR(10) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL
)

CREATE TABLE agendamento_evento (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cpf_morador INT REFERENCES morador(cpf) NOT NULL -- Chave Estrangeira, para mostrar quem foi o responsável pela locação
    data date NOT NULL,
    local int NOT NULL, -
    ambientes VARCHAR(30) CHECK('churrasqueira', 'salão de festas') NOT NULL -- sugestão para substituir o atributo local acima
    apartamento VARCHAR(10) NOT NULL
);

CREATE TABLE visitantes_apartamento (
    cpf_visitante INT PRIMARY KEY,
    cpf_morador INT REFERENCES moradores(cpf) NOT NULL, -- chave estrangeira referenciada da tabela moradores
    nome VARCHAR(50),
    apartamento VARCHAR(10)
);

CREATE TABLE visitantes_eventos (
    cpf_visitante INT PRIMARY KEY,
    cpf_morador INT REFERENCES moradores(cpf) NOT NULL, -- chave estrangeira referenciada da tabela moradores
    nome VARCHAR(50),
    apartamento VARCHAR(10)
)