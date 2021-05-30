FROM python:3.8.5-slim-buster

LABEL maintainer="Liza"
WORKDIR ./todo
RUN pip install poetry

COPY pyproject.toml nginx.conf ./
COPY poetry.lock ./

RUN mkdir -p /todo/todo/
RUN touch /todo/todo/__init__.py

RUN poetry install -n


COPY ./todo /todo/todo

EXPOSE 8000