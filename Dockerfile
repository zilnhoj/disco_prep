FROM python:3.9-slim AS build

WORKDIR /home/app

ENV GUNICORN_CMD_ARGS="0.0.0.0:$PORT --timeout 10"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
COPY govuk-frontend-flask.py .
copy app.json .
copy build.sh .
copy config.py .

RUN ./build.sh

CMD gunicorn govuk-frontend-flask:app
