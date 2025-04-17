import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()
## tentativa de inclusão de valores testes
cur.execute("INSERT INTO usuarios (nome, email, cpf , senha) VALUES (?,?,?,?)",
            ('Gabriel', 'emailGabriel@email.com' , '265.568.987-41' , '1111')
            )

cur.execute("INSERT INTO usuarios (nome, email, cpf , senha) VALUES (?,?,?,?)",
            ('Fabiana', 'emailFabiana@email.com' , '288.354.458-81' , '2222')
            )

connection.commit()
connection.close()