#!/usr/bin/env bash
set -ex

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py test
python3 manage.py runserver
