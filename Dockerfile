# Используйте официальный образ Python как базовый
FROM python:3.10

# Установите рабочую директорию в контейнере
WORKDIR /app

# Копируйте файлы проекта в контейнер
COPY . .

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запустите бота при запуске контейнера
CMD ["python", "./bot.py"]
