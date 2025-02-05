docker compose build
docker compose run --rm web manage.py migrate
docker compose run --rm web manage.py loaddata seeds.json
docker compose up