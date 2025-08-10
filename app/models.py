# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base
from datetime import datetime


class Article(Base):
    __tablename__ = "articles"  # Имя таблицы в БД

    # Поля таблицы
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)  # Ограничение длины
    content = Column(Text, nullable=False)  # Для больших текстов
    author = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Автоматическое время

    def __repr__(self):
        return f"<Article(id={self.id}, title='{self.title}')>"