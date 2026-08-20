web: python3 -m gunicorn -c gunicorn.conf.py
worker: python3 manage.py db_worker
release: python3 manage.py migrate
