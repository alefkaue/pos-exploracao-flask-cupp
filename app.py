# app.py - Aplicacao Flask com dois niveis de acesso (admin e aluno)
# Rodar: python app.py   -> http://127.0.0.1:5000
#
# - admin: ve todos os alunos e PODE editar as notas
# - aluno: ve apenas os dados/notas, SEM poder alterar

import sqlite3
from flask import Flask, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "chave-insegura-apenas-para-laboratorio"

DB = "escola.db"


def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


# ---------------------------------------------------------------- LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        login = request.form.get("login", "")
        senha = request.form.get("senha", "")
        con = db()
        u = con.execute(
            "SELECT * FROM usuarios WHERE login=? AND senha=?", (login, senha)
        ).fetchone()
        con.close()
        if u:
            session["login"] = u["login"]
            session["papel"] = u["papel"]
            return redirect(url_for("painel"))
        else:
            # 401 ajuda o script de brute force a diferenciar sucesso de falha
            erro = "Credenciais invalidas"
            return pagina_login(erro), 401
    return pagina_login(erro)


def pagina_login(erro=""):
    return f"""
    <h2>Login - Sistema Escolar</h2>
    <form method="post">
        Usuario: <input name="login"><br>
        Senha:   <input type="password" name="senha"><br>
        <button type="submit">Entrar</button>
    </form>
    <p style="color:red">{erro}</p>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------- PAINEL
@app.route("/painel")
def painel():
    if "papel" not in session:
        return redirect(url_for("login"))

    con = db()
    alunos = con.execute("SELECT * FROM alunos ORDER BY id").fetchall()
    con.close()

    admin = session["papel"] == "admin"
    html = f"<h2>Painel ({session['login']} - papel: {session['papel']})</h2>"
    html += '<a href="/logout">Sair</a><hr>'
    html += "<table border=1 cellpadding=4><tr>"
    html += "<th>ID</th><th>Nome</th><th>Nascimento</th><th>Endereco</th>"
    html += "<th>Celular</th><th>Materias</th><th>Nota</th>"
    if admin:
        html += "<th>Editar nota</th>"
    html += "</tr>"

    for a in alunos:
        html += "<tr>"
        html += f"<td>{a['id']}</td><td>{a['nome']}</td><td>{a['nascimento']}</td>"
        html += f"<td>{a['endereco']}</td><td>{a['celular']}</td><td>{a['materias']}</td>"
        html += f"<td>{a['nota']}</td>"
        if admin:
            html += f"""<td>
                <form method="post" action="/editar">
                    <input type="hidden" name="id" value="{a['id']}">
                    <input name="nota" size="4" value="{a['nota']}">
                    <button type="submit">Salvar</button>
                </form></td>"""
        html += "</tr>"
    html += "</table>"

    if not admin:
        html += "<p><i>Acesso de aluno: somente leitura.</i></p>"
    return html


# ---------------------------------------------------------------- EDITAR (so admin)
@app.route("/editar", methods=["POST"])
def editar():
    # Bloqueio no servidor: aluno nao consegue editar nem forcando o POST
    if session.get("papel") != "admin":
        return "Acesso negado: apenas administrador pode editar notas.", 403

    id_ = request.form.get("id")
    nota = request.form.get("nota")
    con = db()
    con.execute("UPDATE alunos SET nota=? WHERE id=?", (nota, id_))
    con.commit()
    con.close()
    return redirect(url_for("painel"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
