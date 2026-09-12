import sqlite3

conexao = sqlite3.connect("filmes.db")
cursor = conexao.cursor()

cursor.execute("""
UPDATE usuarios
SET admin = 1
WHERE id = 1
""")

conexao.commit()
conexao.close()

print("Usuário virou administrador!")