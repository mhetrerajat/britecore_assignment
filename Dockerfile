FROM python:3.7

LABEL MAINTAINER="Rajat Mhetre <mhetrerajat@gmail.com>"

RUN groupadd -r api_group && useradd -r -g api_group api_user

WORKDIR /app

COPY . /app

ENV SECRET_KEY="48tkMdPi-dPyIdqGtwGqYbG-argF699U1-H46XmEmU0="

ENV FLASK_APP=run.py
ENV FLASK_ENV=docker

ENV DEV_DATABASE_URL=sqlite:////tmp/britecore_dev.db
ENV TEST_DATABASE_URL=sqlite:////tmp/britecore_test.db
ENV DATABASE_URL=sqlite:////tmp/britecore.db

RUN pip install pipenv
RUN pipenv install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["sh", "-x", "entrypoint.sh"]

