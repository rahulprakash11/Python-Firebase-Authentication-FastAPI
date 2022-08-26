# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster as requirements-stage


ENV  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.1.13

# 1st stage
WORKDIR /tmp

# 
RUN pip install "poetry==$POETRY_VERSION"

# 
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 2nd stage
FROM python:3.8-slim-buster

# 
WORKDIR /testauthapi-docker

# 
COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt


COPY . .


EXPOSE $PORT


CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker main:app
