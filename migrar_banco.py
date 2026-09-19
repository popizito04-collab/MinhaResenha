
import sqlite3
import psycopg2

# =========================
# CONECTAR NO SQLITE
# =========================

sqlite = sqlite3.connect("filmes.db")
sqlite_cursor = sqlite.cursor()

# =========================
# PEGAR A URL DO NEON
# =========================

database_url = input("Cole aqui a DATABASE_URL do Neon: ")

postgres = psycopg2.connect(database_url)
postgres_cursor = postgres.cursor()

print("Conectado ao Neon!")

# =========================
# MIGRAR USUÁRIOS
# =========================

sqlite_cursor.execute("SELECT id, nome, email, senha, admin, foto FROM usuarios")
usuarios = sqlite_cursor.fetchall()

for usuario in usuarios:
    postgres_cursor.execute("""
        INSERT INTO usuarios (id, nome, email, senha, admin, foto)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, usuario)

print(f"{len(usuarios)} usuários migrados!")

# =========================
# MIGRAR FILMES
# =========================

sqlite_cursor.execute("""
    SELECT id, titulo, ano, genero, sinopse, imagem
    FROM filmes
""")

filmes = sqlite_cursor.fetchall()

for filme in filmes:
    postgres_cursor.execute("""
        INSERT INTO filmes (id, titulo, ano, genero, sinopse, imagem)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, filme)

print(f"{len(filmes)} filmes migrados!")

# =========================
# MIGRAR RESENHAS
# =========================

sqlite_cursor.execute("""
    SELECT id, usuario_id, filme_id, texto, nota, data
    FROM resenhas
""")

resenhas = sqlite_cursor.fetchall()

for resenha in resenhas:
    postgres_cursor.execute("""
        INSERT INTO resenhas
        (id, usuario_id, filme_id, texto, nota, data)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, resenha)

print(f"{len(resenhas)} resenhas migradas!")

# =========================
# CORRIGIR SEQUÊNCIAS
# =========================

postgres_cursor.execute("""
    SELECT setval(
        'usuarios_id_seq',
        COALESCE((SELECT MAX(id) FROM usuarios), 1)
    )
""")

postgres_cursor.execute("""
    SELECT setval(
        'filmes_id_seq',
        COALESCE((SELECT MAX(id) FROM filmes), 1)
    )
""")

postgres_cursor.execute("""
    SELECT setval(
        'resenhas_id_seq',
        COALESCE((SELECT MAX(id) FROM resenhas), 1)
    )
""")

# =========================
# SALVAR
# =========================

postgres.commit()

sqlite.close()
postgres.close()

print()
print("================================")
print("MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
print("================================")