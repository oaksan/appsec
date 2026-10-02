# Zeppelin-AppSec: Modelo de Evolução e Instrumento de Diagnóstico

Instrumento de avaliação e diagnóstico de maturidade DevSecOps baseado no modelo evolutivo **StH-AppSec** (*Stairway to Heaven*) e na hierarquia industrial **Purdue / ISA-95**, com rastreabilidade ao **OWASP SAMM v2.0** e **OWASP DSOMM v5.0.2** (IFES, 2026).

---

## 🚀 Como Executar Localmente

Você pode executar o sistema de duas maneiras no seu computador:
1. **Via Python / Ambiente Virtual (`venv`)** - Direto na máquina.
2. **Via Docker / Docker Compose** - Totalmente isolado em container (não precisa instalar Python nem pacotes).

---

### Opção 1: Execução com Python (Recomendado)

#### Pré-requisitos
- **Python 3.10, 3.11, 3.12 ou 3.13** instalado.
- Gerenciador de pacotes `pip`.

#### Passo a Passo no Linux / macOS:
```bash
# 1. Entre na pasta do projeto
cd appsec

# 2. Crie um ambiente virtual limpo
python3 -m venv .venv

# 3. Ative o ambiente virtual
source .venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Inicie o servidor
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Passo a Passo no Windows (PowerShell / Prompt de Comando):
```powershell
# 1. Entre na pasta do projeto
cd appsec

# 2. Crie um ambiente virtual
python -m venv .venv

# 3. Ative o ambiente virtual
# No PowerShell:
.venv\Scripts\Activate.ps1
# Ou no CMD:
.venv\Scripts\activate.bat

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Inicie o servidor
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

### Opção 2: Execução com Docker

Se o computador de destino tiver o Docker instalado, basta um comando:

```bash
docker compose up --build
```

Ou usando Docker diretamente:
```bash
# Construir imagem
docker build -t zeppelin-appsec .

# Executar container na porta 8000
docker run -d -p 8000:8000 --name zeppelin-appsec zeppelin-appsec
```

---

## 🌐 Acesso ao Sistema

Após iniciar o servidor, abra o navegador e acesse:
- **Painel Analítico / Dashboard**: [http://localhost:8000](http://localhost:8000)
- **Documentação Interativa da API (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Especificação OpenAPI (Redoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Executando os Testes Automatizados

Para certificar a integridade matemática e operacional de todos os módulos:

```bash
pytest tests/ -v
```

A suíte executará os 29 testes automatizados com validação canônica dos dados da dissertação.

---

## 📁 Estrutura do Projeto

- `main.py`: Aplicação FastAPI, rotas REST, Jinja2 e ciclo de vida (`lifespan`).
- `models.py`: Entidades SQLModel/Pydantic, regras de validação e funções matemáticas do StH-AppSec.
- `database.py`: Conexão SQLite (WAL mode, Foreign Keys) e rotina de carga inicial (`seed_database`).
- `requirements.txt`: Dependências do ecossistema Python.
- `templates/`: Interface HTML responsiva renderizada via Jinja2 e Tailwind CSS.
- `static/`: Lógica do cliente (`app.js`) com Chart.js e interações assíncronas via `fetch`.
- `docs/`: Planilhas canônicas da dissertação para carga inicial e documento de referência (`SDL.pdf`).
- `tests/`: Bateria de testes unitários e de integração (`pytest`).
- `specs/`: Especificações executáveis e documentação de arquitetura.
- `zeppelin.db`: Banco de dados SQLite persistente.
