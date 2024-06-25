# Базовый образ
FROM python:3.12-alpine

# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файлов зависимостей
COPY .. /app

# Установка poetry и зависимостей проекта
RUN pip install -r requirements.txt

# Делаем entrypoint скрипт исполняемым
RUN chmod +x entrypoint.sh

RUN python manage.py collectstatic --noinput --clear

# Установка entrypoint
ENTRYPOINT ["sh", "entrypoint.sh"]
