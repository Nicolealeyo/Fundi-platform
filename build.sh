#!/usr/bin/env bash
set -o errexit

# Render runs this before collectstatic; dependencies are not auto-installed for this build command.
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate --noinput

