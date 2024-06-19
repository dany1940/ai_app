# Pull base image
FROM python:3.12

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

ADD pyproject.toml .

# install poetry, don't use Python to ensure that poetry deps are separated from python deps
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

# install dependencies from poetry
# disable creating virtual env as Docker is already a clean slate
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev


COPY . /app/

EXPOSE 8000
