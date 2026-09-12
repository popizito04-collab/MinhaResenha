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