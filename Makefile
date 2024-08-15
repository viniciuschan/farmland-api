# Development shortcuts
lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

test:
	docker-compose exec farmland-api su -c "poetry run pytest -sx"

deps:
	docker-compose exec farmland-api su -c "poetry install"

run:
	docker-compose up

drop:
	docker-compose down

migrations:
	docker-compose exec farmland-api su -c "python manage.py makemigrations"

migrate:
	docker-compose exec farmland-api su -c "python manage.py migrate"
