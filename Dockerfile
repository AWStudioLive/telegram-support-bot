# Берем официальный чистый и очень легкий образ Python
FROM python:3.14-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Чтобы Python не кэшировал .pyc файлы внутри контейнера
ENV PYTHONDONTWRITEBYTECODE=1
# Чтобы логи выводились в консоль Docker сразу, без задержек (буферизации)
ENV PYTHONUNBUFFERED=1

# Копируем и устанавливаем зависимости (кэшируем этот слой для быстрой сборки)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь остальной код бота в контейнер
COPY . .

# Запускаем скрипт бота
CMD ["python", "main.py"]