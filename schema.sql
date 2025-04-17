DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome text not null,
    email text not null,
    cpf text not null,
    senha text not null
);