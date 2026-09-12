import sqlite3

conexao = sqlite3.connect("filmes.db")
cursor = conexao.cursor()

cursor.execute("ALTER TABLE filmes ADD COLUMN imagem TEXT")

cursor.execute("""
UPDATE filmes
SET imagem = 'interestelar.jpg'
WHERE id = 1
""")

cursor.execute("""
UPDATE filmes
SET imagem = 'poderoso-chefao.jpg'
WHERE id = 2
""")

conexao.commit()
conexao.close()

print("Imagens adicionadas!")