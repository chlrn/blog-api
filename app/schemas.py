# app/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Базовый класс для статьи (без ID и времени создания)
class ArticleBase(BaseModel):
    title: str = Field(..., max_length=100, example="Заголовок статьи")
    content: str = Field(..., example="Содержание статьи")
    author: str = Field(..., max_length=50, example="Автор статьи")


# Схема для создания статьи (наследует базовый)
class ArticleCreate(ArticleBase):
    pass


# Полная схема статьи (включает ID и время создания)
class Article(ArticleBase):
    id: int
    created_at: datetime

    # Настройка для работы с ORM объектами
    class Config:
        orm_mode = True


# Схема для обновления статьи (все поля необязательные)
class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100, example="Новый заголовок")
    content: Optional[str] = Field(None, example="Новое содержание")
    author: Optional[str] = Field(None, max_length=50, example="Новый автор")