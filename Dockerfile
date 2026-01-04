FROM python:3.11-slim

WORKDIR /app

# Instala dependências essenciais para drivers de banco
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tudo de 'src' para o WORKDIR (/app)
COPY . .

# Faz o Python tratar /app como raiz para encontrar auth, books, etc.
ENV PYTHONPATH=/app

# O comando usa main_teste porque é o nome do seu arquivo na imagem
CMD ["sh", "-c", "alembic upgrade head && uvicorn main_teste:app --host 0.0.0.0 --port 8000"]