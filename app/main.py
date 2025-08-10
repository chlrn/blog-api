# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .routers import articles

# Создаем таблицы в БД (для разработки)
# В продакшене используйте миграции (Alembic)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Блог API",
    description="REST API для управления статьями блога",
    version="1.0.0",
)

# Подключаем роутер статей с префиксом /api/v1/articles
app.include_router(
    articles.router,
    prefix="/api/v1/articles",
    tags=["Статьи"]
)

@app.get("/", include_in_schema=False)
def root():
    return {"message": "Добро пожаловать в API блога! Перейдите на /docs для документации."}

# Зависимость для проверки подключения к БД
@app.get("/healthcheck", include_in_schema=False)
def healthcheck(db: Session = Depends(get_db)):
    try:
        # Простая проверка подключения к БД
        db.execute("SELECT 1")
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}