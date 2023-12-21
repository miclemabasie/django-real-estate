ifneq (,$(wildcard ./.env))
	include .env
	export
	ENV_FILE_PARAM = --env-file .env

endif


build:
	docker-compose up --build -d --remove-orphans

up:	
	docker-compose up -d

down:
	docker-compose down

show-logs:
	docker-compose logs


migrate:
	docker-compose exec api python manage.py migrate

makemigrations:
	docker-compose exec api python manage.py makemigrations

createsuperuser:
	docker-compose exec api python manage.py createsuperuser

collecstatic:
	docker-compose exec api python manage.py collectstatic --no-input --clear

django-check:
	docker-compose exec api python manage.py check

shell:	
	docker-compose exec api python manage.py shell

down-v:
	docker-compose down -v 

volume:
	docker volume inspect django-real-estate_postgres_data


estate-db:
	docker-compose exec postgres-db psql -U miclem -d realestate_learn

test:
	docker-compose exec api pytest -p no:warnings --cov=.

test-html:
	docker-compose exec api pytest -p no:warnings --cov=. --cov-report html

flake8:
	docker-compose exec api flake8

black-check:
	docker-compose exec api black --check --exclude=migrations .

black-diff:
	docker-compose exec api black --diff --exclude=migrations .

black:
	docker-compose exec api black --exclude=migrations .

isort-check:
	docker-compose exec api isort . --check-only --skip env --skip migrations

isort-diff:
	docker-compose exec api isort . --diff --skip env --skip  migrations
	
isort:
	docker-compose exec api isort . --skip env --skip migrations

lint: 
	flake8 black-check isort-check


watch:
	docker-compose exec api watchmedo shell-command --patterns="*.py" --recursive --command='make lint test' .