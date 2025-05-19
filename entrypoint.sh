#!/bin/sh

echo "🛠 Генерация миграций..."
python manage.py makemigrations --noinput

echo "📦 Применение миграций..."
python manage.py migrate --noinput

echo "🎯 Сбор статических файлов..."
python manage.py collectstatic --noinput

echo "🚀 Запуск Gunicorn..."
exec "$@"
