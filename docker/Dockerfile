FROM python:3.11 as base

ENV C_FORCE_ROOT=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

WORKDIR /code

RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir poetry==1.8.3

COPY pyproject.toml /code/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev \
    && echo yes | poetry cache clear . --all


# tests image
FROM base AS test

RUN poetry install --no-interaction --no-ansi --with dev
