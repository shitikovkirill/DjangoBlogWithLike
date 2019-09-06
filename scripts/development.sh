#!/usr/bin/env bash
tox -e devenv
source /app/venv/bin/activate
python manage.py makemigrations
python manage.py migrate
python /app/manage.py runserver 0.0.0.0:8000
