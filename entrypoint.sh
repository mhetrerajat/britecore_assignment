#!/bin/sh
pipenv run flask db migrate
pipenv run flask db upgrade
pipenv run flask initdb
pipenv run flask import sample_data.csv
pipenv run flask run --host=0.0.0.0
