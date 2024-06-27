# Базовый образ
FROM python:3.12-alpine

# Установка зависимостей системы
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk add jpeg-dev zlib-dev libjpeg \
    && apk del build-deps
# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файлов зависимостей
COPY . /app

# Установка зависимостей проекта
RUN pip install --no-cache-dir -r requirements.txt

# Делаем entrypoint скрипт исполняемым
RUN chmod +x entrypoint.sh

# Установка entrypoint
ENTRYPOINT ["sh", "entrypoint.sh"]
