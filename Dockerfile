FROM python:3.9-slim AS build

WORKDIR /home/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ./build.sh
copy disco_prep/ disco_prep/
COPY govuk-frontend-flask.py .



# CMD gunicorn govuk-frontend-flask:app
CMD gunicorn -b 127.0.0.1:5000 --timeout 10 govuk-frontend-flask:app
