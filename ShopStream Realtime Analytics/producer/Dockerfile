FROM python:3.11-slim

WORKDIR /app

COPY producer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY producer/ .

COPY data/raw/ /app/data/raw/

ENV PYTHONUNBUFFERED=1

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app