#!/bin/bash

# Проверка доступности базы данных с помощью dockerize
echo "Waiting for the database to be ready..."
dockerize -wait tcp://${DB_HOST}:${DB_PORT:-5432} -timeout 30s


# Выполнение миграций
echo "Running database migrations..."
alembic upgrade head

# Запуск приложения
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload