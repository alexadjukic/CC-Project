FROM python

ENV PORT=8000

WORKDIR /app

COPY /app .

COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT fastapi dev --host 0.0.0.0 --port ${PORT} main.py
