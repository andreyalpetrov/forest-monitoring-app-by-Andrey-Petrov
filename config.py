import os
from datetime import timedelta

class Config:
    """Конфигурация Flask приложения"""
    
    # PostgreSQL подключение
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://forest_user:forest_pass@db:5432/forest_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask параметры
    JSON_SORT_KEYS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Загрузка файлов
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB лимит
