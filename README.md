# Books API — Tech Challenge

Este projeto foi desenvolvido como proposta de solução ao Tech Challenge, especificamente ao desafio da 1ª Fase da Pós Tech em Machine Learning Engineering. O desafio consite em raspar os dados do site [Books to Scrape](https://books.toscrape.com/) e disponibilizar esses dados para interação via API.

## Arquitetura

O diagrama abaixo é um esboço da arquitetura da solução implementada. Mais detalhes sobre essa arquitetura e sobre o funcionamento da API podem ser encontrados neste [vídeo](https://www.youtube.com/watch?v=FeoGBGLzZtY).

![Fluxo dos dados](/assets/tech_challenge-diagrama_arq-books_api.png)

## Deploy - Produção

Esta aplicação está hospedada no [Render](https://render.com/), e sua documentação pode ser acessada em https://fiap-tech-challenge-books-api.onrender.com/docs. O Render facilita bastante o processo de deploy, sendo necessário pouca configuração adicional. Dentre as etapas de configuração, destacam-se:

Build Command: `poetry install --no-root`\
Start Command: `uvicorn books_api.main:app --host 0.0.0.0 --port $PORT`

Além disso, são cadastradas as seguintes variáveis de ambiente:

`PYTHONPATH=./src`\
`PYTHON_VERSION=3.12.11`

`POSTGRES_HOST=`_omitido por segurança_\
`POSTGRES_PORT=5432`\
`POSTGRES_DB=prd-postgres`\
`POSTGRES_USER=`_omitido por segurança_\
`POSTGRES_PASSWORD=`_omitido por segurança_

`ADMIN_USER=admin`\
`ADMIN_PASSWORD=`_omitido por segurança_

`SECRET_KEY=`_omitido por segurança_

## Deploy - Desenvolvimento (local)

Requisitos:
- [git](https://git-scm.com/)
- [Python](https://www.python.org/) >= 3.12 (recomenda-se o uso do [pyenv](https://github.com/pyenv/pyenv) para gerenciar diferentes versões de Python)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/) (opcional, utilizado neste projeto para prover uma instância postgres)

Início rápido:
1. Clonar repositório: `git clone https://github.com/yuriperim/FIAP-tech_challenge-books_api.git books_api`
2. Entrar no diretório do projeto: `cd books_api`
3. Instalar dependências: `poetry install`
4. Ativar ambiente virtual: `poetry shell` (em caso de erro, verificar comando [`poetry env activate`](https://python-poetry.org/docs/cli/#env-activate))
5. Subir banco de dados (opcional): `docker compose --env-file .env.development up -d` (caso o desenvolvedor tenha acesso a uma instância postgres, pode-se adaptar os arquivos do projeto para apontar para essa instância)
6. Adicionar tabelas do banco de dados (pode ser realizada posteriormente, ver passo 8): `alembic upgrade head` (uma das causas de erro nessa etapa pode ser a não ativação do ambiente virtual, nesse caso tentar o comando `poetry run alembic upgrade head`)
7. Subir aplicação: `PYTHONPATH=./src uvicorn books_api.main:app --reload` (em caso de erro, verificar se o ambiente virtual foi ativado corretamente, ou preceder o comando `uvicorn` com `poetry run`)
8. Adicionar tabelas do banco de dados (pode ter sido realizada anteriormente, ver passo 6): executar endpoint `/api/v1/migrations/up` (necessário autenticar, usuário e senha estão no arquivo `.env.development`, variáveis `ADMIN_USER` e `ADMIN_PASSWORD`)

Obs.: para derrubar a aplicação, apertar `Ctrl + C`; para derrubar o banco de dados, utilizar o comando `docker compose --env-file .env.development down`

## Principais pastas e responsabilidades
- src/books_api
  - configs — carregamento de variáveis de ambiente e disponibilização de configurações para a aplicação
  - models — camada de banco de dados
  - services — camada com serviço de ETL, e funções utilitárias para hashing de senhas e geração/decodificação de JWT
  - routers — definição dos endpoint da API, separados em _admin_ e _books_

Outros arquivos importantes
- pyproject.toml — arquivo de dependências
- compose.yaml — arquivo para subida de uma instância postgres, já com volume configurado
