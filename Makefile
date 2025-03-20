reset-index:
	docker compose run backend python manage.py search_index --delete -f
	docker compose run backend python manage.py search_index --rebuild -f

migrate:
	docker compose run backend python manage.py makemigrations
	docker compose run backend python manage.py migrate

test:
	docker compose run backend python manage.py test

clean-docker:
	docker compose down --rmi all -v --remove-orphans

recreate-db:
	docker compose down -v
	docker compose up -d postgres
	docker compose run backend python manage.py makemigrations
	docker compose run backend python manage.py migrate
	docker compose run backend python manage.py createsuperuser
