#!/bin/sh

python3 manage.py migrate --noinput || exit 1

python3 manage.py loaddata seeds.json 

exec "$@"
