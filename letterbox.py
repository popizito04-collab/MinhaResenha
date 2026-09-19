from werkzeug.security import generate_password_hash, check_password_hash
import os
import psycopg2
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
app.secret_key = "minha-chave-secreta"


def conectar():
    return psycopg2.connect(os.environ["DATABASE_URL"])


@app.route("/admin/editar-filme/<int:id>", methods=["GET", "POST"])
def editar_filme(id):

    if session.get("admin") != 1:
        return "Acesso negado!", 403

    conexao = conectar()
    cursor = conexao.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        ano = request.form["ano"]
        genero = request.form["genero"]
        sinopse = request.form["sinopse"]

        imagem = request.files["imagem"]

        if imagem and imagem.filename:

            nome_imagem = secure_filename(imagem.filename)

            pasta = "static/imagens"

            imagem.save(os.path.join(pasta, nome_imagem))

            cursor.execute("""
                UPDATE filmes
                SET titulo = %s,
                    ano = %s,
                    genero = %s,
                    sinopse = %s,
                    imagem = %s
                WHERE id = %s
            """, (
                titulo,
                ano,
                genero,
                sinopse,
                nome_imagem,
                id
            ))

        else:

            cursor.execute("""
                UPDATE filmes
                SET titulo = %s,
                    ano = %s,
                    genero = %s,
                    sinopse = %s
                WHERE id = %s
            """, (
                titulo,
                ano,
                genero,
                sinopse,
                id
            ))

        conexao.commit()
        conexao.close()

        return redirect(url_for("admin"))

    cursor.execute(
        "SELECT * FROM filmes WHERE id = %s",
        (id,)
    )

    filme = cursor.fetchone()

    conexao.close()

    return render_template(
        "editar_filme.html",
        filme=filme
    )


@app.route("/admin/adicionar-filme", methods=["POST"])
def adicionar_filme():

    if session.get("admin") != 1:
        return "Acesso negado!", 403

    titulo = request.form["titulo"]
    ano = request.form["ano"]
    genero = request.form["genero"]
    sinopse = request.form["sinopse"]

    imagem = request.files["imagem"]

    nome_imagem = secure_filename(imagem.filename)

    pasta = "static/imagens"

    imagem.save(os.path.join(pasta, nome_imagem))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO filmes (titulo, ano, genero, sinopse, imagem)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        titulo,
        ano,
        genero,
        sinopse,
        nome_imagem
    ))

    conexao.commit()
    conexao.close()

    return redirect(url_for("admin"))


@app.route("/admin/excluir-resenha/<int:id>", methods=["POST"])
def excluir_resenha(id):

    if session.get("admin") != 1:
        return "Acesso negado!", 403

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM resenhas WHERE id = %s",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect(url_for("admin"))


@app.route("/admin/nota-filme/<int:filme_id>", methods=["POST"])
def nota_filme(filme_id):

    if session.get("admin") != 1:
        return "Acesso negado!", 403

    nota = request.form["nota"]

    try:
        nota = float(nota)
    except ValueError:
        return "Nota inválida!", 400

    if nota < 0 or nota > 10:
        return "A nota deve estar entre 0 e 10!", 400

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO nota_turma (filme_id, nota)
        VALUES (%s, %s)
        ON CONFLICT (filme_id)
        DO UPDATE SET nota = EXCLUDED.nota
    """, (
        filme_id,
        nota
    ))

    conexao.commit()
    conexao.close()

    return redirect(url_for("admin"))

@app.route("/admin")
def admin():

    if session.get("admin") != 1:
        return "Acesso negado!", 403

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM filmes")
    filmes = cursor.fetchall()

    cursor.execute("""
        SELECT resenhas.id,
               resenhas.texto,
               resenhas.nota,
               usuarios.nome,
               filmes.titulo
        FROM resenhas
        JOIN usuarios
            ON resenhas.usuario_id = usuarios.id
        JOIN filmes
            ON resenhas.filme_id = filmes.id
        ORDER BY resenhas.id DESC
    """)

    resenhas = cursor.fetchall()

    conexao.close()

    return render_template(
        "admin.html",
        filmes=filmes,
        resenhas=resenhas
    )


@app.route("/filmes")
def filmes():

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM filmes")
    filmes = cursor.fetchall()

    cursor.execute("SELECT nota FROM nota_turma LIMIT 1")
    resultado = cursor.fetchone()

    if resultado:
        nota_turma = resultado[0]
    else:
        nota_turma = None

    conexao.close()

    return render_template(
        "letterbox.html",
        filmes=filmes,
        nota_turma=nota_turma
    )


@app.route("/filme/<int:id>/resenha", methods=["POST"])
def enviar_resenha(id):

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    texto = request.form["texto"]

    try:
        nota = float(request.form["nota"])

        elenco = float(request.form["elenco"])
        direcao = float(request.form["direcao"])
        roteiro = float(request.form["roteiro"])
        figurino = float(request.form["figurino"])
        trilha_sonora = float(request.form["trilha_sonora"])

    except (ValueError, TypeError):
        return """
        <h2>Você precisa avaliar todas as categorias ⭐</h2>
        <p>Escolha as estrelas para Elenco, Direção, Roteiro, Figurino e Trilha sonora.</p>
        <a href="javascript:history.back()">Voltar</a>
        """, 400

    media_categorias = (
        elenco +
        direcao +
        roteiro +
        figurino +
        trilha_sonora
    ) / 5

    usuario_id = session["usuario_id"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO resenhas
        (
            usuario_id,
            filme_id,
            texto,
            nota,
            elenco,
            direcao,
            roteiro,
            figurino,
            trilha_sonora,
            media_categorias
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        usuario_id,
        id,
        texto,
        nota,
        elenco,
        direcao,
        roteiro,
        figurino,
        trilha_sonora,
        media_categorias
    ))

    conexao.commit()
    conexao.close()

    return redirect(url_for("filme", id=id))

@app.route("/admin/resenhas")
def admin_resenhas():

    if session.get("admin") != 1:
        return "Acesso negado!", 403

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT resenhas.id,
               resenhas.texto,
               resenhas.nota,
               usuarios.nome,
               filmes.titulo
        FROM resenhas
        JOIN usuarios
            ON resenhas.usuario_id = usuarios.id
        JOIN filmes
            ON resenhas.filme_id = filmes.id
        ORDER BY resenhas.id DESC
    """)

    resenhas = cursor.fetchall()

    conexao.close()

    return render_template(
        "admin_resenhas.html",
        resenhas=resenhas
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s",
            (email,)
        )

        usuario = cursor.fetchone()

        conexao.close()

        if usuario:

            if usuario[3] == senha:

                session["usuario_id"] = usuario[0]
                session["usuario_nome"] = usuario[1]
                session["admin"] = usuario[4]

                if session["admin"] == 1:
                    return redirect(url_for("admin"))

                return redirect(url_for("filmes"))

            elif check_password_hash(usuario[3], senha):

                session["usuario_id"] = usuario[0]
                session["usuario_nome"] = usuario[1]
                session["admin"] = usuario[4]

                if session["admin"] == 1:
                    return redirect(url_for("admin"))

                return redirect(url_for("filmes"))

        return "Email ou senha incorretos!"

    return render_template("login.html")






@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        conexao = conectar()
        cursor = conexao.cursor()

        senha_hash = generate_password_hash(senha)

        cursor.execute("""
            INSERT INTO usuarios
            (nome, email, senha)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (
            nome,
            email,
            senha_hash
        ))

        usuario_id = cursor.fetchone()[0]

        conexao.commit()
        conexao.close()

        # Já deixa o usuário logado
        session["usuario_id"] = usuario_id
        session["usuario_nome"] = nome
        session["admin"] = 0

        return redirect(url_for("filmes"))

    return render_template("cadastro.html")
@app.route("/")
def inicio():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM filmes")
    filmes = cursor.fetchall()

    cursor.execute("SELECT nota FROM nota_turma LIMIT 1")
    resultado = cursor.fetchone()

    if resultado:
        nota_turma = resultado[0]
    else:
        nota_turma = None

    conexao.close()

    return render_template(
        "letterbox.html",
        filmes=filmes,
        nota_turma=nota_turma
    )



@app.route("/filme/<int:id>")
def filme(id):

    conexao = conectar()
    cursor = conexao.cursor()

    # Busca o filme
    cursor.execute(
        "SELECT * FROM filmes WHERE id = %s",
        (id,)
    )

    filme = cursor.fetchone()


    # Busca as resenhas
    cursor.execute("""
        SELECT resenhas.texto,
               resenhas.nota,
               usuarios.nome
        FROM resenhas
        JOIN usuarios
            ON resenhas.usuario_id = usuarios.id
        WHERE resenhas.filme_id = %s
        ORDER BY resenhas.id DESC
    """, (id,))

    resenhas = cursor.fetchall()


    # Calcula a média geral das categorias
    cursor.execute("""
        SELECT AVG(media_categorias)
        FROM resenhas
        WHERE filme_id = %s
    """, (id,))

    resultado = cursor.fetchone()

    media_filme = resultado[0]


    # Converte de 0-5 para 0-10
    if media_filme is not None:
        media_filme = round(float(media_filme) * 2, 1)


    conexao.close()

    return render_template(
        "filme.html",
        filme=filme,
        resenhas=resenhas,
        media_filme=media_filme
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)