FROM python:3-slim

RUN mkdir -p /data/log
RUN mkdir -p /data/src

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:5000 --log-level=info main:app