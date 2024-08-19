lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

test:
	docker-compose exec farmland-api su -c "poetry run pytest -sx"

migrations:
	docker-compose exec farmland-api su -c "python manage.py makemigrations"

migrate:
	docker-compose exec farmland-api su -c "python manage.py migrate"

create_user:
	docker-compose exec farmland-api su -c "python manage.py createsuperuser"

load_fixtures:
	docker-compose exec farmland-api su -c "python manage.py loaddata src/fixtures/locations.json"
	docker-compose exec farmland-api su -c "python manage.py loaddata src/fixtures/farmers.json"
	docker-compose exec farmland-api su -c "python manage.py loaddata src/fixtures/farms.json"

shell:
	docker-compose exec farmland-api su -c "python manage.py shell"

run:
	docker-compose up -d

drop:
	docker-compose down
