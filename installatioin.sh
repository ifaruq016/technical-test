#!/bin/sh
cp .env.example .env 
pip3 install pipenv
pipenv --three
source $(pipenv --venv)/bin/activate
pipenv install
source run.sh