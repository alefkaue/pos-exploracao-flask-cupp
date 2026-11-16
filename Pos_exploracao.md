# Pós-exploração em sistemas

**Professor:** Paulo Alexandre Martin

---

## 1. Pós-exploração em sistemas

- A pós-exploração é a fase posterior à invasão do sistema. Nesta situação, o objetivo é entender o ambiente, expandir privilégios e movimentar-se pela rede.
- Em um teste de invasão, a pós-exploração é a etapa mais importante porque revela o nível de dados que a vulnerabilidade permite.
- Após um acesso, o invasor procura descobrir: usuário atual, grupo de permissões, sistema operacional, patches instalados, processos em execução, serviços ativos e configurações de rede.
- O primeiro acesso, geralmente, é feito como usuário comum e somente depois será feita uma tentativa de obter permissões administrativas.

## 2. Enumeração de usuários

- Na enumeração de usuários, o objetivo é identificar as contas existentes no sistema.
- As informações de interesse são: nome do usuário, identificador (UID/SID), status da conta, último login, diretório pessoal e tipo da conta.
- Algumas contas pertencem a serviços. Essas contas frequentemente possuem acesso a arquivos sensíveis e podem se tornar alvos valiosos caso estejam mal configuradas.
- Os grupos permitem facilitar o gerenciamento de permissões. Imagine um grupo de professores: ao invés de configurar permissões para cada professor, podemos configurar permissões uma única vez para o grupo. Portanto, automaticamente, todos os professores têm as mesmas permissões.

## 3. Grupos

*Exemplo de grupos, usuários e permissões — sistema escolar (Flask + MySQL). Conteúdo do diagrama da página 4:*

| Usuário | UID | Função | Grupo |
|---|---:|---|---|
| `admin` | 1000 | Administrador do sistema | Administradores |
| `professor01` | 1001 | Professor | Professores |
| `professor02` | 1002 | Professora | Professores |
| `aluno01` | 1003 | Aluno | Alunos |
| `aluno02` | 1004 | Aluno | Alunos |
| `backupsvc` | 1005 | Conta de serviço (backup) | Serviços |
| `mysql` | 1006 | Conta de serviço (banco de dados) | Serviços |
| `flaskapp` | 1007 | Conta de serviço (aplicação) | Serviços |

### Permissões e acessos por grupo

| Grupo | Nível indicado no diagrama | Permissões |
|---|---|---|
| **Administradores** | Full Control | Criar, editar e excluir usuários; gerenciar banco de dados; acessar todos os arquivos e configurações; configurar o sistema. |
| **Professores** | Modify | Visualizar notas (todas as turmas); lançar e editar notas; acessar material didático; visualizar relatórios acadêmicos. |
| **Alunos** | Read | Visualizar suas próprias notas; acessar materiais de estudo; participar de atividades; sem permissão para alterar dados. |
| **Serviços** | Execute | Acessar banco de dados (`mysql`); acessar arquivos da aplicação (`flaskapp`); executar tarefas de backup (`backupsvc`); sem acesso interativo (login desabilitado). |

**Princípio do menor privilégio:** cada usuário deve ter apenas as permissões necessárias para realizar suas atividades.

## 4. Escalonamento de privilégios

- O escalonamento de privilégios ocorre quando um usuário ou processo obtém permissões superiores às originalmente concedidas.
- **Escalonamento vertical:** o usuário obtém um nível mais alto de privilégio do que o nível anterior.
- **Escalonamento horizontal:** o usuário passa a acessar outra conta com o mesmo nível de privilégio, mas pertencente a outra pessoa ou função.
- Para o escalonamento vertical, a descoberta da senha é um caminho. Entretanto, existem outros caminhos como SQL Injection, credenciais expostas ou arquivos de backup esquecidos.

### Escalonamento vertical e horizontal — diagrama da página 6

| Escalonamento vertical | Escalonamento horizontal |
|---|---|
| Obtenção de um nível mais alto de privilégio. | Acesso a outras contas no mesmo nível de privilégio. |
| Ocorre quando um usuário consegue privilégios maiores do que os que possuía inicialmente. | Ocorre quando um usuário acessa outra conta com o mesmo nível de privilégio, sem necessariamente obter mais direitos. |
| **Hierarquia ilustrada:** Usuário comum → Usuário avançado → Administrador → SYSTEM/root. | **Movimento lateral ilustrado:** Usuário A ↔ Usuário B ↔ Usuário C, com acesso a seus respectivos arquivos. |
| **Exemplos:** usuário comum obtém privilégios de administrador; conta de aplicação obtém acesso de `root`; usuário com poucos direitos passa a ter controle total do sistema. | **Exemplos:** acesso aos arquivos de outro usuário comum; acesso a outra conta de funcionário no mesmo departamento; acesso a caixas postais de outros usuários; acesso a recursos de outros usuários em uma aplicação. |

## 5. Criação de lista de palavras (wordlist)

- A **wordlist** é uma lista organizada de palavras, nomes, padrões e combinações que pode ser usada em atividades de auditoria de segurança autorizadas, análise de senhas e treinamentos de conscientização.
- Na fase de pós-exploração e enumeração, o objetivo conceitual da criação de uma wordlist é aproveitar informações coletadas sobre a organização para entender riscos associados a senhas previsíveis.

**Exemplo apresentado:**

- **Empresa:** XYZ
- **Cidade:** São Paulo
- **Ano de fundação:** 2000

Possíveis padrões de senha:

```text
XYZ123
xyz123
XYZ@123
xyz@123
XYZ2000
xyz2000
XYZ2026
```

## 6. Common User Passwords Profiler (CUPP)

- **CUPP** (*Common User Passwords Profiler*) é uma ferramenta de geração de wordlists personalizadas baseada em informações conhecidas sobre um usuário ou organização. Ela foi criada para avaliações de segurança autorizadas e auditorias de senhas, gerando listas de palavras a partir de nomes, datas, apelidos, empresas, hobbies e outros dados coletados durante a enumeração.
- O CUPP faz perguntas sobre o perfil do usuário e gera automaticamente combinações plausíveis de senhas.
- O CUPP é frequentemente utilizado em cursos para mostrar que muitos usuários criam senhas baseadas em informações pessoais previsíveis.
- O CUPP não é uma ferramenta online. Ele é um programa escrito em Python que normalmente é executado localmente em um computador.
- **GitHub:** https://github.com/Mebus/cupp

## 7. Crunch e CeWL

### Crunch

- **Crunch** é uma ferramenta de linha de comando muito conhecida em laboratórios de segurança para gerar wordlists por combinação de caracteres, seguindo padrões definidos pelo usuário.
- O Crunch é um programa compilado para linha de comando, não um script Python.
- Normalmente já está disponível nos repositórios das distribuições voltadas para segurança, como Kali Linux.

### CeWL

- **CeWL** significa *Custom Word List Generator*.
- É uma ferramenta que percorre páginas de um site e extrai palavras encontradas no conteúdo para gerar uma wordlist personalizada.
- O CeWL foi desenvolvido em Ruby, portanto não é um script Python.
- **Projeto oficial:** https://github.com/digininja/CeWL

## 8. CUPP, Crunch e CeWL — quadro comparativo

*Informações do diagrama da página 10. O quadro original agrupa CUPP e Crunch em uma coluna e compara essa abordagem ao CeWL.*

| Aspecto | CUPP / Crunch | CeWL |
|---|---|---|
| **Origem dos dados** | Informações pessoais do alvo, coletadas manualmente ou durante a exploração. | Conteúdo de sites (páginas web). |
| **Tipo de informação** | Dados de pessoas: nome, apelido, datas etc. | Palavras do site: institucionais, técnicas etc. |
| **Abordagem** | Personalizada e direcionada. | Automatizada e baseada em conteúdo web. |
| **Como funciona** | O CUPP solicita dados e gera combinações inteligentes; o Crunch pode gerar variações e combinações por outros métodos. | Acessa o site, extrai palavras, aplica filtros, remove caracteres especiais e gera uma wordlist. |
| **Ponto forte** | Gera listas altamente personalizadas e relevantes para o alvo específico. | Rápido e eficiente para obter palavras relacionadas a uma empresa, projeto ou tema. |
| **Quando usar** | Quando já existem informações sobre o usuário (pós-exploração, engenharia social, enumeração etc.). | Quando o objetivo é gerar uma lista a partir de um site (empresa, blog, portal institucional). |

**Exemplos de uso apresentados no diagrama:**

```bash
python3 cupp.py
```

```bash
cewl -w lista.txt https://exemplo.com
```

> “Quanto mais informações você tiver, mais eficaz será a wordlist.”

> O CeWL é indicado para extrair palavras de sites e transformar conteúdo em uma wordlist.

**Na pós-exploração:** ambas as ferramentas ajudam na criação de wordlists para testes de força bruta (por exemplo: SSH, RDP, VPN), mas são usadas em contextos diferentes. O material destaca que ferramentas diferentes têm o mesmo objetivo: aumentar as chances de sucesso nos testes de segurança.

## 9. Atividade

1. Crie uma página com **Flask no Python**. Esta página deve pedir nome de usuário e senha para permitir acesso de **administrador** ou acesso de **aluno** (deve ter dois níveis de acesso).
2. O acesso de administrador deve permitir a modificação das notas dos alunos. Crie um banco de dados pequeno com nomes dos alunos, data de nascimento, endereço, celular e matérias cursadas. Você pode usar o **MySQL** ou **SQLite** no Python.
3. O acesso de aluno permite apenas a visualização dos dados pessoais e notas. Nenhuma alteração pode ser feita utilizando este acesso.
4. Utilize **CUPP** para gerar uma lista com senhas. Crie uma senha fraca para o acesso de administrador e o acesso de aluno nesta página implementada com Flask.
5. A partir da lista gerada pelo CUPP, implemente uma aplicação em Python que tenta acessar o site automaticamente.
6. Apresente o código em Python e os testes de invasão utilizando CUPP em um arquivo **PDF**. Fazer **individualmente**.

---

*Transcrição adaptada para Markdown do material “Pós-exploração em sistemas” (11 páginas). Os diagramas das páginas 4, 6 e 10 foram convertidos para tabelas e descrições textuais para manter o conteúdo acessível em um arquivo `.md` independente.*
