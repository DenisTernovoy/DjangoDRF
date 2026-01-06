# Указываем базовый образ
FROM python:3.13

# Устанавливаем рабочую директорию в контейнере
WORKDIR ./

RUN pip install poetry

# Копируем файл с зависимостями и устанавливаем их
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Копируем остальные файлы проекта в контейнер
COPY . .

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000

# Определяем команду для запуска приложения
ENTRYPOINT ["poetry", "run"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]