# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Используем переменную окружения из docker-compose
DATABASE_URL = "postgresql://postgres:postgres@db:5432/blog_db"

# Создаем движок SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создаем фабрику сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Функция для получения сессии БД (будет использоваться в зависимостях)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()