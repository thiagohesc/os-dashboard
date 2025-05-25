# Autor: Thiago Costa
# Data: 25/05/2025
# Disciplina: Sistemas Operacionais - UTFPR
# Dockerfile para montar a imagem do backend da aplicacao

FROM python:3.11-slim

WORKDIR /app

COPY ./app /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]