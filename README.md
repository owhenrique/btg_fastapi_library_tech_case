# Biblioteca — Case técnico BTG 📚

**Descrição**

Case técnico desenvolvido para o BTG. É uma API REST construída com FastAPI que gerencia uma pequena biblioteca: livros, usuários e empréstimos, com autenticação via JWT, controle de permissões, testes e configuração para linting e formatação.

---

## ✅ Funcionalidades

- CRUD de **livros** (Book)
- CRUD de **usuários** (User) com controle de papéis/roles
- Gerenciamento de **empréstimos** (Lending)
- **Autenticação** via JWT
- **Rate limiting** (middleware)
- **Logging** e tratamento centralizado de exceções
- Suíte de **testes** com cobertura

---

## 🛠 Tecnologias

- Python >= 3.13
- FastAPI
- SQLAlchemy
- aiosqlite (Banco em sqlite assíncrono para simplicidade)
- python-jose (JWT)
- ruff (lint/format)
- pytest (testes)

---

## ▶️ Como rodar localmente

1. Clone o repositório

```bash
git clone <repo-url>
cd repo-name
```

2. Instale as dependências (recomendado via Poetry)

```bash
# instalar o Poetry se necessário
poetry install
```

3. Rodar em modo de desenvolvimento

```bash
poetry run task dev
# ou, alternativamente
poetry run uvicorn app.main:app --reload
```

4. A API fornece um endpoint de saúde em `/health` e os endpoints da aplicação estão em `/api` (ver rotas no código). A documentação automática do FastAPI estará disponível em `/docs` (Swagger) quando o servidor estiver rodando.

## ⚙️ Configuração de ambiente

O projeto utiliza variáveis de ambiente para configuração. Crie um arquivo `.env` na raiz do projeto com base no template fornecido (`.env.template`).

Exemplo de variáveis no `.env`:

```env
APP_ENV=development
CREATE_DEV_ADMIN=true
```

Quando `CREATE_DEV_ADMIN=true`, um usuário admin é criado automaticamente ao iniciar o projeto.

O template `.env.template` serve como referência para todas as variáveis necessárias.

---

## 📑 Documentação das rotas

Toda a documentação das rotas está disponível automaticamente via Swagger em [`/docs`](http://localhost:8000/docs) quando o servidor está rodando.

## 🗂️ Estrutura do Projeto

O projeto está organizado nos seguintes módulos:

- `app/core/` — Configurações, exceções, logging, segurança, rate limiting
- `app/db/` — Banco de dados, fixtures e inicialização
- `app/models/` — Modelos ORM: Book, User, Lending
- `app/repositories/` — Repositórios para acesso aos dados
- `app/services/` — Regras de negócio e serviços
- `app/api/v1/` — Rotas da API (auth, books, lendings, users)
- `app/main.py` — Ponto de entrada da aplicação FastAPI
- `tests/` — Testes automatizados e factories

Outros arquivos importantes:

- `.env.template` — Exemplo de variáveis de ambiente
- `pyproject.toml` — Configuração de dependências, tasks e linters

## ✅ Comandos úteis (definidos em `pyproject.toml` via taskipy)

> Observação: use `poetry run` caso esteja usando Poetry.

- `poetry run task lint` — executa `ruff check`
- `poetry run task pre_format` — executa `ruff check --fix` (checagens e tentativas de correção)
- `poetry run task format` — executa `ruff format`
- `poetry run task dev` — executa `fastapi dev app/main.py` (modo desenvolvimento)
- `poetry run task test` — executa `pytest -s -x --cov=app -vv` (testes com cobertura)

Também é possível executar diretamente:

- `ruff check .` / `ruff format .`
- `pytest`
- `uvicorn app.main:app --reload`

Configurações principais do `ruff` estão em `pyproject.toml` (ex.: `line-length = 79`, seletores e opções de formatação).

---

## 🧪 Testes & Cobertura

- Rode: `poetry run task test`
- Após os testes, o relatório de cobertura em HTML é gerado em `htmlcov/` (com `coverage html`) — ver `post_test` no `pyproject.toml`.

---

## ✍️ Autor

**Paulo Almeida** — me.pauloalmeida@gmail.com

---

## Contribuições

Sinta-se à vontade para abrir issue ou PR com melhorias, correções de bugs ou sugestões.
