# gerar_pdf.py - monta o PDF de entrega com o codigo e os testes de invasao
# Uso: python gerar_pdf.py
# Gera: Atividade_Pos_Exploracao.pdf

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak, Image
)
from reportlab.lib.utils import ImageReader

styles = getSampleStyleSheet()
h1 = styles["Heading1"]
h2 = styles["Heading2"]
normal = styles["BodyText"]
code = ParagraphStyle("code", fontName="Courier", fontSize=7, leading=8.5)

doc = SimpleDocTemplate(
    "Atividade_Pos_Exploracao.pdf", pagesize=A4,
    leftMargin=1.5 * cm, rightMargin=1.5 * cm,
    topMargin=1.5 * cm, bottomMargin=1.5 * cm,
)

flow = []


def titulo(t):
    flow.append(Paragraph(t, h1))
    flow.append(Spacer(1, 6))


def sub(t):
    flow.append(Spacer(1, 6))
    flow.append(Paragraph(t, h2))
    flow.append(Spacer(1, 4))


def texto(t):
    flow.append(Paragraph(t, normal))
    flow.append(Spacer(1, 4))


def bloco_codigo(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()
    flow.append(Preformatted(conteudo, code))
    flow.append(Spacer(1, 8))


def bloco_texto(txt):
    flow.append(Preformatted(txt, code))
    flow.append(Spacer(1, 8))


def imagem(caminho, legenda=""):
    # encaixa a imagem na largura util mantendo a proporcao
    larg_util = A4[0] - 3 * cm
    ir = ImageReader(caminho)
    iw, ih = ir.getSize()
    w = larg_util
    h = ih * (w / iw)
    flow.append(Image(caminho, width=w, height=h))
    if legenda:
        flow.append(Paragraph(f"<i>{legenda}</i>", normal))
    flow.append(Spacer(1, 10))


# ----------------------------------------------------------- CAPA / INTRO
titulo("Atividade - Pos-exploracao em sistemas")
texto("Disciplina: Pos-exploracao em sistemas &nbsp;|&nbsp; Prof. Paulo Alexandre Martin")
texto(
    "Resumo: aplicacao web em Flask com dois niveis de acesso (administrador e aluno) "
    "sobre um banco SQLite. O administrador edita as notas; o aluno apenas visualiza. "
    "Senhas fracas foram criadas de proposito e constam da wordlist gerada pelo CUPP. "
    "Um script em Python usa essa wordlist para realizar forca bruta no login e demonstrar "
    "o risco de senhas previsiveis. Ambiente 100% local e autorizado (laboratorio)."
)

sub("Credenciais (senhas fracas, presentes na wordlist do CUPP)")
bloco_texto(
    "admin   / paulo1985   -> papel: admin (edita notas)\n"
    "aluno01 / rex2010      -> papel: aluno (somente leitura)"
)

sub("Como executar")
bloco_texto(
    "1) python init_db.py            # cria o banco escola.db\n"
    "2) python app.py                # sobe o site em http://127.0.0.1:5000\n"
    "3) Gerar wordlist com o CUPP:\n"
    "   python cupp.py -i < respostas.txt   (perfil: paulo/martin/pet rex/empresa escola)\n"
    "   -> gera paulo.txt (copiado como wordlist.txt)\n"
    "4) python brute_force.py admin   wordlist.txt\n"
    "   python brute_force.py aluno01 wordlist.txt"
)

# ----------------------------------------------------------- CUPP
flow.append(PageBreak())
titulo("Geracao da wordlist com o CUPP")
texto(
    "A wordlist foi gerada pelo CUPP (Common User Passwords Profiler) a partir de um "
    "perfil ficticio do alvo. As respostas usadas foram:"
)
bloco_texto(
    "First Name ....... paulo\n"
    "Surname .......... martin\n"
    "Nickname ......... paulo\n"
    "Birthdate ........ 01011985\n"
    "Pet's name ....... rex\n"
    "Company name ..... escola\n"
    "(demais campos em branco; sem keywords, special chars, random ou leet)"
)
texto("Saida real da execucao do CUPP:")
bloco_texto(open("saida_cupp.txt", encoding="utf-8").read())
texto(
    "As senhas fracas cadastradas no sistema (admin: paulo1985, aluno01: rex2010) "
    "aparecem nessa wordlist, o que torna o ataque de forca bruta viavel."
)

# ----------------------------------------------------------- CODIGO
flow.append(PageBreak())
titulo("Codigo-fonte")

sub("init_db.py - criacao do banco SQLite")
bloco_codigo("init_db.py")

sub("app.py - site Flask (dois niveis de acesso)")
bloco_codigo("app.py")

sub("brute_force.py - ataque de forca bruta usando a wordlist")
bloco_codigo("brute_force.py")

# ----------------------------------------------------------- TELAS
flow.append(PageBreak())
titulo("Funcionamento do sistema (telas)")
sub("Tela de login")
imagem("screenshots/01_login.jpg", "Formulario de login (usuario e senha).")
sub("Acesso ADMINISTRADOR - edita notas")
imagem("screenshots/02_painel_admin.jpg",
       "Painel do admin: coluna 'Editar nota' com campo e botao Salvar em cada aluno.")
sub("Acesso ALUNO - somente leitura")
imagem("screenshots/03_painel_aluno.jpg",
       "Painel do aluno: sem coluna de edicao; aviso 'Acesso de aluno: somente leitura'.")

# ----------------------------------------------------------- TESTES
flow.append(PageBreak())
titulo("Testes de invasao")

sub("1. Forca bruta descobrindo a senha do ADMIN")
bloco_texto(open("saida_admin.txt", encoding="utf-8").read())

sub("2. Forca bruta descobrindo a senha do ALUNO")
bloco_texto(open("saida_aluno.txt", encoding="utf-8").read())

sub("3. Controle de acesso (aluno NAO pode editar; admin pode)")
bloco_texto(open("saida_acl.txt", encoding="utf-8").read())

sub("Conclusao")
texto(
    "O CUPP, a partir de poucos dados do alvo (nome, pet, empresa, datas), gerou uma lista "
    "com ~1100 senhas. Como as senhas do admin e do aluno eram previsiveis, ambas foram "
    "encontradas em poucos segundos. Isso confirma, na pratica, a importancia do uso de "
    "senhas fortes e de bloqueio de tentativas repetidas de login."
)

doc.build(flow)
print("PDF gerado: Atividade_Pos_Exploracao.pdf")
