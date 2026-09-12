import sqlite3

conexao = sqlite3.connect("filmes.db")

cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS resenhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    filme_id INTEGER NOT NULL,
    texto TEXT NOT NULL,
    nota INTEGER NOT NULL,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conexao.commit()

conexao.close()

print("Tabela de resenhas criada!")