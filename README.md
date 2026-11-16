# Atividade - Pós-exploração em sistemas

Atividade da disciplina **Pós-exploração em sistemas** (Prof. Paulo Alexandre Martin).

Aplicação web em **Flask + SQLite** com dois níveis de acesso (administrador e aluno) e
um script de **força bruta** que usa uma wordlist gerada pelo **CUPP** para demonstrar o
risco de senhas fracas/previsíveis.

> ⚠️ Ambiente de laboratório, 100% local e autorizado. As senhas fracas e o uso de força
> bruta existem apenas para fins didáticos. Não use contra sistemas de terceiros.

## Estrutura

| Arquivo | Descrição |
|---|---|
| `init_db.py` | Cria o banco `escola.db` (usuários e alunos). |
| `app.py` | Site Flask com login e dois níveis de acesso. |
| `brute_force.py` | Ataque de força bruta no login usando a wordlist. |
| `gerar_pdf.py` | Gera o PDF de entrega (código + testes + telas). |
| `wordlist.txt` | Wordlist gerada pelo CUPP. |
| `cupp_tool/` | CUPP (clonado de github.com/Mebus/cupp) + `respostas.txt` do perfil usado. |
| `screenshots/` | Telas do sistema em funcionamento. |
| `Atividade_Pos_Exploracao.pdf` | Entrega final. |
| `Pos_exploracao.md` | Material da disciplina transcrito. |

## Credenciais (senhas fracas, propositais)

| Usuário | Senha | Papel |
|---|---|---|
| `admin` | `paulo1985` | admin (edita notas) |
| `aluno01` | `rex2010` | aluno (somente leitura) |

## Como executar

```bash
python init_db.py            # cria o banco escola.db
python app.py                # sobe o site em http://127.0.0.1:5000

# gerar a wordlist com o CUPP (perfil em cupp_tool/respostas.txt)
cd cupp_tool && python cupp.py -i < respostas.txt && cp paulo.txt ../wordlist.txt && cd ..

# ataque de força bruta
python brute_force.py admin   wordlist.txt
python brute_force.py aluno01 wordlist.txt
```

## Requisitos

- Python 3
- `flask`, `requests`, `reportlab` (`pip install flask requests reportlab`)
