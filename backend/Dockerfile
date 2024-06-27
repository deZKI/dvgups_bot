# Базовый образ
FROM python:3.12-alpine

# Установка зависимостей системы
RUN apk update && \
    apk add --no-cache \
    bash \
    libjpeg \
    zlib

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файлов зависимостей
COPY . /app

# Установка зависимостей проекта
RUN pip install --no-cache-dir -r requirements.txt

# Делаем entrypoint скрипт исполняемым
RUN chmod +x entrypoint.sh

# Сборка статических файлов Django
RUN python manage.py collectstatic --noinput --clear

# Установка entrypoint
ENTRYPOINT ["sh", "entrypoint.sh"]
