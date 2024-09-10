#!/bin/bash
set -e

python3 manage.py wait_for_db

python3 manage.py wait_for_redis

python3 manage.py migrate

python3 manage.py collectstatic --no-input --clear

gunicorn FX.wsgi:application -c gunicorn_conf.py
