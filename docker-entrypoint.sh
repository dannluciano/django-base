#!/bin/sh

if [ "$APP" = "web" ]; then
    echo "==> Migrating Database"
    python3 manage.py migrate --noinput || exit 1

    echo "==> Loading Data do Database"
    python3 manage.py loaddata seeds.json 

    echo "==> Creating Bucket"
    python3 manage.py create_bucket
fi

exec "$@"
