<!-- Copilot instructions for this Django base project -->
# Repo overview

This is a small Django project scaffold used as a base template. Key facts an AI coding agent should know to be productive:

- **Framework**: Django (project scaffold in `{{project_name}}/`); main apps are `core` and `base`.
- **Runtime**: Development target uses `docker-compose` with services: `web`, `worker`, `db` (Postgres), `minio` (S3-compatible), and `mail` (MailPit). See `docker-compose.yml`.
- **Background tasks**: Uses `django_tasks` with a DB-backed worker. Worker is started via `python3 manage.py db_worker` (see `docker-compose` `worker` service).
- **Storage**: Uses `django-storages` and `whitenoise` for static files. In local dev `minio` provides an S3 endpoint (see `settings.py` and `docker-compose.yml`).
- **Frontend conventions**: Uses `django-htmx` and `crispy-bulma`. Views often switch templates when `request.htmx` is true (see `core/views.py` — `with_template` decorator and `base_template` logic).

# What to look for when editing or adding code

- Follow app boundaries: add new views, models, and templates inside the relevant app directory (`core/`, `base/`). URL wiring follows Django conventions in `core/urls.py` and `{{project_name}}/urls.py`.
- Background work: enqueue long-running work with `task` functions (see `core/tasks.py`) and test by running the `db_worker` locally or in the `worker` container.
- Settings/config: project uses `python-decouple` for secrets and `dj_database_url` for DB configuration. Default `settings.py` contains S3/minio defaults — prefer environment variables in `.env` for sensitive values.
- Static assets: `STATIC_ROOT` is `assets/` and `collectstatic` runs during the Docker build (`Dockerfile.dev`). Be mindful when changing static file names — the project uses `CompressedManifestStaticFilesStorage` for production-style static handling.

# Useful repo-specific commands

- Start full dev stack (from repo root):

```
docker-compose up --build
```

- Run only Django dev server (inside container):

```
python3 manage.py runserver 0.0.0.0:8000
```

- Run background worker locally or in container:

```
python3 manage.py db_worker
```

- Build image used by `web`/`worker` (dev):

```
docker build -f Dockerfile.dev -t django-base:dev .
```

- Collect static files (run inside the container / build step):

```
python3 manage.py collectstatic --no-input
```

- Apply migrations and create admin user (usual Django flow):

```
python3 manage.py migrate
python3 manage.py createsuperuser
```

# Patterns & examples to use in code suggestions

- HTMX-aware views: prefer returning context dicts and using the `with_template` decorator pattern shown in `core/views.py`. If `request.htmx` is True use `main.html` as the base template.
- Enqueue emails and tasks via `send_email.enqueue(...)` or decorate small functions with `@task()` (see `core/tasks.py`). Suggest using small, testable tasks that don't import heavy app state.
- Read runtime config via `decouple.config(...)` and `extra_settings` when appropriate (`Setting.get('...')`) rather than hardcoding values.

# Files to consult for context

- `{{project_name}}/settings.py` — project settings, storage, middleware, installed apps
- `docker-compose.yml`, `Dockerfile.dev`, `docker-entrypoint.sh` — development environment and container lifecycle
- `core/views.py`, `core/tasks.py`, `core/urls.py` — typical view/task patterns and URL layout
- `requirements.txt` — main dependencies to consider when suggesting libraries

# What not to change without confirmation

- Don't change storage/backing service choices (S3/minio, whitenoise) without coordinating; many infra pieces assume S3-compatible endpoints.
- Avoid altering authentication URL patterns; the project uses built-in `django.contrib.auth` patterns and `accounts/` routes.

# When you need more info

- Ask the user for their intended environment (local container vs host Python) before suggesting run/debug instructions.
- If tests or CI are required, request access to the CI config (not present in this repo) before adding CI-specific steps.

---
If any section is unclear or you'd like more examples (tests, a sample HTMX flow, or a task unit test), tell me which part to expand.
