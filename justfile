set shell := ["powershell.exe", "-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command"]

# Show available commands.
default:
    @just --list

# Show available commands.
help:
    @just --list
# --- Dev server ---

run:
    uv run manage.py runserver

shell:
    uv run manage.py shell

# --- Database ---

db-up:
    docker compose up -d pg

db-down:
    docker compose down

db-logs:
    docker compose logs -f pg

db-shell:
    docker compose exec pg psql -U ${DB_USER} -d ${DB_NAME}

# --- Migrations ---

migrate:
    uv run manage.py migrate

makemigrations app='':
    uv run manage.py makemigrations {{ app }}

showmigrations:
    uv run manage.py showmigrations

# --- Testing ---

test:
    uv run pytest

test-fast:
    uv run pytest --no-cov -x

test-file file:
    uv run pytest {{ file }} --no-cov -v

# --- Lint & Format ---

lint:
    uv run ruff check .

fmt:
    uv run ruff format .

fmt-check:
    uv run ruff format --check .

typecheck:
    uv run mypy .

check: lint fmt-check typecheck

# --- Pre-commit ---

pre-commit:
    uv run pre-commit run --all-files

pre-commit-install:
    uv run pre-commit install

# --- Dependencies ---

sync:
    uv sync --all-groups

lock:
    uv lock

add pkg:
    uv add {{ pkg }}

add-dev pkg:
    uv add --group dev {{ pkg }}

# --- Django utils ---

createsuperuser:
    uv run manage.py createsuperuser

collectstatic:
    uv run manage.py collectstatic --noinput

check-deploy:
    uv run manage.py check --deploy
