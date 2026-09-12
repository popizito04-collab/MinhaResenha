import sqlite3

conexao = sqlite3.connect("filmes.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL
)
""")

conexao.commit()
conexao.close()

print("TESTE FUNCIONANDO")

import sqlite3

conexao = sqlite3.connect("filmes.db")
cursor = conexao.cursor()

cursor.execute("""
ALTER TABLE usuarios
ADD COLUMN admin INTEGER DEFAULT 0
""")

conexao.commit()
conexao.close()

print("Coluna admin criada!")