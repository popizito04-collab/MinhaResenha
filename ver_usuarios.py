import sqlite3

conexao = sqlite3.connect("filmes.db")
cursor = conexao.cursor()

cursor.execute("SELECT * FROM usuarios")

usuarios = cursor.fetchall()

for usuario in usuarios:
    print(usuario)

conexao.close()