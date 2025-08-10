# app/routers/articles.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import get_db

router = APIRouter()


@router.post("/",
             response_model=schemas.Article,
             status_code=status.HTTP_201_CREATED,
             summary="Создать новую статью",
             tags=["Статьи"])
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    """
    Создает новую статью в блоге.

    - **title**: Заголовок статьи (макс. 100 символов)
    - **content**: Содержание статьи
    - **author**: Автор статьи (макс. 50 символов)
    """
    return crud.create_article(db, article)


@router.get("/",
            response_model=list[schemas.Article],
            summary="Получить список статей",
            tags=["Статьи"])
def read_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Возвращает список статей с пагинацией.

    - **skip**: Количество статей для пропуска (по умолчанию 0)
    - **limit**: Максимальное количество статей для возврата (по умолчанию 10)
    """
    return crud.get_articles(db, skip=skip, limit=limit)


@router.get("/{article_id}",
            response_model=schemas.Article,
            summary="Получить статью по ID",
            tags=["Статьи"])
def read_article(article_id: int, db: Session = Depends(get_db)):
    """
    Возвращает статью по указанному ID.

    - **article_id**: ID статьи (целое число)
    """
    article = crud.get_article(db, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Статья с ID {article_id} не найдена"
        )
    return article


@router.put("/{article_id}",
            response_model=schemas.Article,
            summary="Обновить статью",
            tags=["Статьи"])
def update_article(article_id: int, article: schemas.ArticleUpdate, db: Session = Depends(get_db)):
    """
    Обновляет существующую статью.

    - **article_id**: ID статьи для обновления
    - **title**: Новый заголовок (опционально)
    - **content**: Новое содержание (опционально)
    - **author**: Новый автор (опционально)
    """
    db_article = crud.update_article(db, article_id, article)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Статья с ID {article_id} не найдена"
        )
    return db_article


@router.delete("/{article_id}",
               response_model=schemas.Article,
               summary="Удалить статью",
               tags=["Статьи"])
def delete_article(article_id: int, db: Session = Depends(get_db)):
    """
    Удаляет статью по указанному ID.

    - **article_id**: ID статьи для удаления
    """
    db_article = crud.delete_article(db, article_id)
    if not db_article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Статья с ID {article_id} не найдена"
        )
    return db_article