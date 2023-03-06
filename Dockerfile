FROM python:3.9-slim AS build

WORKDIR /home/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ./build.sh

CMD gunicorn govuk-frontend-flask:app
