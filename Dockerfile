FROM python:3.7

LABEL MAINTAINER="Rajat Mhetre <mhetrerajat@gmail.com>"

WORKDIR /app

COPY . /app

ENV SECRET_KEY="48tkMdPi-dPyIdqGtwGqYbG-argF699U1-H46XmEmU0="

ENV FLASK_APP=run.py
ENV FLASK_ENV=docker

ENV DEV_DATABASE_URL=sqlite:////app/britecore_dev.db
ENV TEST_DATABASE_URL=sqlite:////app/britecore_test.db
ENV DATABASE_URL=sqlite:////app/britecore.db

RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt

RUN groupadd -r api_group && useradd -m -d /home/api_user -r -g api_group api_user
RUN chown -R api_user:api_group /app /home/api_user
USER api_user

RUN flask db stamp head
RUN flask db migrate
RUN flask db upgrade
RUN flask initdb
RUN flask import sample_data.csv

CMD gunicorn --workers 1 --bind 0.0.0.0:$PORT run --access-logfile - --error-logfile - --log-level debug

