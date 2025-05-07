import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


cur.execute("INSERT INTO moradores (cpf, nome, apartamento, email, senha) VALUES (?, ?, ?, ?, ?)",
            (22587939745, 'Gabriel', '101', 'gabriel@email.com', '1234'))

cur.execute("INSERT INTO moradores (cpf, nome, apartamento, email, senha) VALUES (?, ?, ?, ?, ?)",
            (28964851257, 'Fabiana', '102', 'fabiana@email.com', '5678'))

connection.commit()
connection.close()
print("Banco criado com sucesso com dados de teste.")
