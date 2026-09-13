from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from werkzeug.utils import secure_filename
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
app.secret_key = "minha-chave-secreta"



@app.route("/admin/editar-filme/<int:id>", methods=["GET", "POST"])
def editar_filme(id):

    if session.get("admin") != 1:
        return "Acesso negado!", 403

    conexao = sqlite3.connect("filmes.db")
    cursor = conexao.cursor()

    if request.method == "POST":

        titulo = request.form["titulo"]
        ano = request.form["ano"]
        genero = request.form["genero"]
        sinopse = request.form["sinopse"]

        imagem = request.files["imagem"]

        # Se o admin escolheu uma nova imagem
        if imagem and imagem.filename:

            nome_imagem = secure_filename(imagem.filename)

            pasta = "static/imagens"

            imagem.save(os.path.join(pasta, nome_imagem))

            cursor.execute("""
                UPDATE filmes
                SET titulo = ?, ano = ?, genero = ?, sinopse = ?, imagem = ?
                WHERE id = ?
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
                SET titulo = ?, ano = ?, genero = ?, sinopse = ?
                WHERE id = ?
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
        "SELECT * FROM filmes WHERE id = ?",
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

    conexao = sqlite3.connect("filmes.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO filmes (titulo, ano, genero, sinopse, imagem)
        VALUES (?, ?, ?, ?, ?)
    """, (titulo, ano, genero, sinopse, nome_imagem))

    conexao.commit()
    conexao.close()

    return redirect(url_for("admin"))

@app.route("/admin/excluir-resenha/<int:id>", methods=["POST"])
def excluir_resenha(id):

    if session.get("admin") != 1:
        return "Acesso negado!", 403

    conexao = sqlite3.connect("filmes.db")
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM resenhas WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

    return redirect(url_for("admin"))

@app.route("/admin")
def admin():

    if session.get("admin") != 1:
        return "Acesso negado!", 403

    conexao = sqlite3.connect("filmes.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM filmes")
    filmes = cursor.fetchall()

    cursor.execute("""
        SELECT resenhas.id, resenhas.texto, resenhas.nota, usuarios.nome, filmes.titulo
        FROM resenhas
        JOIN usuarios ON resenhas.usuario_id = usuarios.id
        JOIN filmes ON resenhas.filme_id = filmes.id
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

    conexao = sqlite3.connect("filmes.db")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM filmes")

    filmes = cursor.fetchall()

    conexao.close()

    return render_template("letterbox.html", filmes=filmes)

@app.route("/filme/<int:id>/resenha", methods=["POST"])


@app.route("/filme/<int:id>/resenha", methods=["POST"])
def enviar_resenha(id):

    if "usuario_id" not in session:
        return redirect(url_for("login"))

    texto = request.form["texto"]
    nota = request.form["nota"]

    usuario_id = session["usuario_id"]

    conexao = sqlite3.connect("filmes.db")
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO resenhas (usuario_id, filme_id, texto, nota)
    VALUES (?, ?, ?, ?)
    """, (usuario_id, id, texto, nota))

    conexao.commit()
    conexao.close()

    return redirect(url_for("filme", id=id))
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conexao = sqlite3.connect("filmes.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
            (email, senha)
        )

        usuario = cursor.fetchone()

        conexao.close()
        if usuario:
            session["usuario_id"] = usuario[0]
            session["usuario_nome"] = usuario[1]
            session["admin"] = usuario[4]
            if session["admin"] == 1:
                return redirect(url_for("admin"))
            return redirect(url_for("filmes"))
        

        else:
            return "Email ou senha incorretos!"

    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        conexao = sqlite3.connect("filmes.db")
        cursor = conexao.cursor()

        cursor.execute("""
        INSERT INTO usuarios (nome, email, senha)
        VALUES (?, ?, ?)
        """, (nome, email, senha))

        conexao.commit()
        conexao.close()

        return "Cadastro realizado com sucesso!"

    return render_template("cadastro.html")




@app.route("/") 
def inicio():
    return render_template("login.html")



@app.route("/filme/<int:id>")
def filme(id):

    conexao = sqlite3.connect("filmes.db")
    cursor = conexao.cursor()

    
    cursor.execute(
        "SELECT * FROM filmes WHERE id = ?",
        (id,)
    )

    filme = cursor.fetchone()

    
    cursor.execute("""
        SELECT resenhas.texto, resenhas.nota, usuarios.nome
        FROM resenhas
        JOIN usuarios ON resenhas.usuario_id = usuarios.id
        WHERE resenhas.filme_id = ?
        ORDER BY resenhas.id DESC
    """, (id,))

    resenhas = cursor.fetchall()

    conexao.close()

    return render_template(
        "filme.html",
        filme=filme,
        resenhas=resenhas
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)