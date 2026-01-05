# Указываем базовый образ
FROM python:latest

# Устанавливаем рабочую директорию в контейнере
WORKDIR ./

RUN pip install poetry

# Копируем файл с зависимостями и устанавливаем их
COPY pyproject.toml poetry.lock README.md ./
RUN poetry install --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Переменные окружения
ENV DJANGO_SECRET_KEY="django-insecure-m@#8a&^j8rwcexi%8qp#iq)&znc&8g*dwk2mpt3#045#t2=xh9"
ENV DJANGO_DEBUG="True"
ENV DB_NAME="djangorf"
ENV DB_USER="postgres"
ENV DB_PASSWORD="12345678910"
ENV DB_HOST="db"
ENV DB_PORT="5432"

ENV CELERY_BROKER_URL="redis://redis:6379/0"
ENV CELERY_RESULT_BACKEND="redis://redis:6379/0"

# Определяем команду для запуска приложения
ENTRYPOINT ["poetry", "run"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]