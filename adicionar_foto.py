import sqlite3

conexao = sqlite3.connect("filmes.db")
cursor = conexao.cursor()

cursor.execute("""
ALTER TABLE usuarios
ADD COLUMN foto TEXT
""")

conexao.commit()
conexao.close()

print("Coluna foto adicionada!")