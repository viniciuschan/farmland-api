# Farmland API
=============

##### Simple API REST to handle and provide some farm data to a dashboard
###### Author: Vinícius Chan

#### Required dependencies
| Dependency | Download Link |
| ------ | ------ |
| Docker | https://docs.docker.com/get-docker/ |
| Git | https://git-scm.com/downloads |
| Postgres 16.4 | https://www.postgresql.org/download/ |
| Poetry 1.8+ | https://pypi.org/project/poetry/ |
| Python 3.12+ | https://www.python.org/downloads/ |
| Django 5.1+ | https://pypi.org/project/Django/ |


# Getting Started
Since this service is running in docker-compose containers, all you need in your machine is Docker and Git.
There are some useful dev commands in the Makefile. So you can run the project locally as it follows:

1. Clone this repository:
```
git clone git@github.com:viniciuschan/farmland-api.git
```

2. To start the service using docker-compose run the following command:
```
make run
```

3. As soon as your containers are up, you must migrate the db structure:
```
make migrate
```

4. Now you check all project test cases by running:
```
make test
```

5. I prepared a sample of initial fixtures to populate the development db.
```
make load_fixtures
```

6. Now you can test the following endpoints, with the sample data I prepared

=============

# About the project: How it works

## Swagger Documentation
Endpoint: **http://localhost:8000/api/docs/**

All the available endpoints and the API contract to manipulate the farmland-api resources are listed in the swagger docs above.

## Summary of the API endpoints
### Farmers:
Endpoint: **http://localhost:8000/api/farmers/**

### Locations:
Endpoint: **http://localhost:8000/api/locations/**

### Farms:
Endpoint: **http://localhost:8000/api/farms/**

### Dashboard:
This is the main feature of the project.
You can make a GET request to this endpoint and it's going to query the current DB to provide some data that allows you to provide a dashboard.

Endpoint: **http://localhost:8000/api/farms/dashboard/**
