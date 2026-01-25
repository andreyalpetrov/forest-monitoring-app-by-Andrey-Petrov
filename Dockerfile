FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY app.py .
COPY models.py .
COPY config.py .

# Создание директории для загрузок
RUN mkdir -p /uploads

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", \
     "--timeout", "120", "--workers", "4", "app:app"]
