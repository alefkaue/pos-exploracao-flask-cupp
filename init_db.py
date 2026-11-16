# init_db.py - cria o banco SQLite e popula com dados de teste
# Executar uma vez: python init_db.py

import sqlite3

con = sqlite3.connect("escola.db")
cur = con.cursor()

# ---- limpa e recria ----
cur.executescript("""
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS alunos;

CREATE TABLE usuarios (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    login    TEXT UNIQUE NOT NULL,
    senha    TEXT NOT NULL,
    papel    TEXT NOT NULL            -- 'admin' ou 'aluno'
);

CREATE TABLE alunos (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    nome          TEXT NOT NULL,
    nascimento    TEXT,
    endereco      TEXT,
    celular       TEXT,
    materias      TEXT,
    nota          REAL
);
""")

# ---- usuarios (senhas FRACAS de proposito - presentes na wordlist do CUPP) ----
# A senha do admin e do aluno sao geradas pelo perfil usado no CUPP.
usuarios = [
    ("admin",       "paulo1985",  "admin"),   # senha fraca do administrador (esta na wordlist do CUPP)
    ("aluno01",     "rex2010",    "aluno"),    # senha fraca do aluno (esta na wordlist do CUPP)
]
cur.executemany("INSERT INTO usuarios (login, senha, papel) VALUES (?,?,?)", usuarios)

# ---- alunos ----
alunos = [
    ("Ana Souza",     "12/03/2008", "Rua A, 100 - Sao Paulo", "(11) 90000-0001", "Matematica, Portugues, Historia", 7.5),
    ("Bruno Lima",    "25/07/2007", "Rua B, 200 - Sao Paulo", "(11) 90000-0002", "Fisica, Quimica, Biologia",      6.0),
    ("Carla Dias",    "03/11/2008", "Rua C, 300 - Sao Paulo", "(11) 90000-0003", "Geografia, Ingles, Educacao Fisica", 8.2),
    ("Diego Alves",   "19/01/2007", "Rua D, 400 - Sao Paulo", "(11) 90000-0004", "Matematica, Fisica, Programacao",  5.4),
]
cur.executemany(
    "INSERT INTO alunos (nome, nascimento, endereco, celular, materias, nota) VALUES (?,?,?,?,?,?)",
    alunos,
)

con.commit()
con.close()
print("Banco 'escola.db' criado com sucesso.")
print("Usuarios:")
print("  admin   / paulo1985  (papel: admin)")
print("  aluno01 / rex2010    (papel: aluno)")
