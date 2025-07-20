FROM python:3.13-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /app .

ENV PORT=8000

ENV PYTHONDONTWRITEBYTECODE=1

ENV ROOT_PATH=/central

ENTRYPOINT fastapi dev --host 0.0.0.0 --port ${PORT} --root-path ${ROOT_PAT} main.py
