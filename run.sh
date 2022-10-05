#!/bin/sh
source $(pipenv --venv)/bin/activate
export FLASK_APP=./serve.py
export FLASK_DEBUG=1
# flask run -h 0.0.0.0
flask run