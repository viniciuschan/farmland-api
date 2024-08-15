FROM python:3.12.5

RUN pip3 install --no-cache --upgrade pip setuptools && pip3 install poetry

ENV PYTHONUNBUFFERED 1

WORKDIR /api
COPY pyproject.toml poetry.lock /api/
RUN poetry config virtualenvs.create false && poetry install

COPY . /api/
