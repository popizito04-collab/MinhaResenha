import sqlite3

conexao = sqlite3.connect("filmes.db")
cursor = conexao.cursor()

email = input("Digite o email do usuário: ")
nova_senha = input("Digite a nova senha: ")

cursor.execute("""
UPDATE usuarios
SET senha = ?
WHERE email = ?
""", (nova_senha, email))

conexao.commit()

print("Senha alterada com sucesso!")

conexao.close()