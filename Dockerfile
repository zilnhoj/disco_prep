# FROM python:3.9-slim AS build

# WORKDIR /home/app

# ENV GUNICORN_CMD_ARGS="0.0.0.0:$PORT --timeout 10"

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY app/ app/
# COPY govuk-frontend-flask.py .
# COPY app.json .
# # copy build.sh .
# COPY config.py .

# # RUN ./build.sh

# CMD gunicorn govuk-frontend-flask:app

FROM python:3.10-slim-buster

LABEL version="1.0"
LABEL maintainer="Data Services"

COPY . /disco_prep
WORKDIR /disco_prep

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 444 *.py
RUN chmod 444 requirements.txt

ENV PORT 8080

EXPOSE 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 govuk-frontend-flask:app
