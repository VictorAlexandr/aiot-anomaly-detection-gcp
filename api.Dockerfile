# api.Dockerfile (Versão com Módulo Python)

# --- Estágio 1: Builder ---
FROM python:3.10-slim as builder
WORKDIR /app
COPY src/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Estágio 2: Final ---
FROM python:3.10-slim
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# --- MUDANÇA IMPORTANTE ---
# Copiamos a pasta 'src' inteira para dentro do container
COPY ./src /app/src
COPY ./artifacts /app/artifacts

# O PYTHONPATH agora aponta para /app, onde a pasta 'src' está
ENV PYTHONPATH=/app

EXPOSE 8000

# --- MUDANÇA CRUCIAL NO COMANDO ---
# Executamos a partir do pacote 'src.api.main'
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]