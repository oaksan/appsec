FROM python:3.11-slim

WORKDIR /app

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar arquivos do projeto
COPY main.py models.py database.py ./
COPY static/ ./static/
COPY templates/ ./templates/
COPY docs/ ./docs/
COPY tests/ ./tests/
COPY specs/ ./specs/
COPY README.md ./

# Porta padrão do Uvicorn / Zeppelin-AppSec
EXPOSE 8000

# Executar aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
