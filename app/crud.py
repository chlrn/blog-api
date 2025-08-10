# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def get_article(db: Session, article_id: int):
    """
    Получить статью по ID
    """
    return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить список статей с пагинацией
    """
    return db.query(models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: schemas.ArticleCreate):
    """
    Создать новую статью
    """
    # Создаем экземпляр модели из данных Pydantic схемы
    db_article = models.Article(
        title=article.title,
        content=article.content,
        author=article.author,
        created_at=datetime.utcnow()  # Устанавливаем текущее время
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)  # Обновляем объект, чтобы получить данные из БД (например, ID)
    return db_article


def update_article(db: Session, article_id: int, article: schemas.ArticleUpdate):
    """
    Обновить существующую статью
    """
    # Получаем статью из БД
    db_article = get_article(db, article_id)
    if not db_article:
        return None

    # Обновляем только переданные поля
    update_data = article.dict(exclude_unset=True)
    for field in update_data:
        setattr(db_article, field, update_data[field])

    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int):
    """
    Удалить статью
    """
    db_article = get_article(db, article_id)
    if not db_article:
        return None

    db.delete(db_article)
    db.commit()
    return db_article