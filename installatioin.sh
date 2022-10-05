#!/bin/sh
pip3 install pipenv
pipenv --three
source $(pipenv --venv)/bin/activate
pipenv install
source run.sh