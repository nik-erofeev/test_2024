FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /example_app

COPY app /example_app/app
COPY docker /example_app/docker
COPY migrations /example_app/migrations
COPY main.py ./
COPY alembic.ini ./
COPY requirements.txt ./
COPY pyproject.toml poetry.lock* ./



RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main



# команда для bush скриптов (чтобы работали)
RUN chmod +x /example_app/docker/app.sh

EXPOSE 8000

