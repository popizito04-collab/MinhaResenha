
import sqlite3

conexao = sqlite3.connect("filmes.db")
cursor = conexao.cursor()

# Apaga a tabela antiga
cursor.execute("DROP TABLE IF EXISTS filmes")

# Cria a tabela novamente
cursor.execute("""
CREATE TABLE filmes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    ano INTEGER,
    genero TEXT,
    sinopse TEXT,
    imagem TEXT
)
""")

# 1 - Interestelar
cursor.execute("""
INSERT INTO filmes (titulo, ano, genero, sinopse, imagem)
VALUES (?, ?, ?, ?, ?)
""", (
    "Interestelar",
    2014,
    "Ficção científica",
    "Uma equipe de astronautas parte em uma missão pelo espaço em busca de um novo lar para a humanidade.",
    "interestelar.jpg"
))

# 2 - O Poderoso Chefão
cursor.execute("""
INSERT INTO filmes (titulo, ano, genero, sinopse, imagem)
VALUES (?, ?, ?, ?, ?)
""", (
    "O Poderoso Chefão",
    1972,
    "Crime",
    "A história da família Corleone e seu envolvimento com o crime organizado.",
    "poderoso-chefao.jpg"
))

# 3 - Cidade de Deus
cursor.execute("""
INSERT INTO filmes (titulo, ano, genero, sinopse, imagem)
VALUES (?, ?, ?, ?, ?)
""", (
    "Cidade de Deus",
    2002,
    "Drama",
    "A história de dois jovens que crescem em uma comunidade marcada pela violência e pelo crime organizado.",
    "cidade-de-deus.jpg"
))

# 4 - A Ilha do Medo
cursor.execute("""
INSERT INTO filmes (titulo, ano, genero, sinopse, imagem)
VALUES (?, ?, ?, ?, ?)
""", (
    "A Ilha do Medo",
    2010,
    "Suspense",
    "Um agente federal investiga o desaparecimento de uma paciente em um hospital psiquiátrico localizado em uma ilha.",
    "ilha-do-medo.jpg"
))

# Salva as alterações
conexao.commit()

# Mostra os filmes cadastrados
cursor.execute("SELECT * FROM filmes")
filmes = cursor.fetchall()

for filme in filmes:
    print(filme)

conexao.close()

print("Banco criado com sucesso!")