#!/bin/sh
pip3 install pipenv
pipenv --three
source $(pipenv --venv)/bin/activate
pipenv install
nohup gunicorn -w 1 -b 0.0.0.0:8000 'app:app' &