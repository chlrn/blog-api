# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.models import Article
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Используем основную базу данных из окружения Docker
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/blog_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Фикстуры для тестов
@pytest.fixture(scope="module")
def db_session():
    # Создаем таблицы
    Article.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(db_session):
    # Переопределяем зависимость get_db для тестов
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Не закрываем сессию явно, чтобы не мешать другим тестам

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture(scope="module")
def test_article(client):
    # Создаем тестовую статью
    response = client.post(
        "/api/v1/articles/",
        json={"title": "Test Article", "content": "Test content", "author": "Test Author"}
    )
    return response.json()


# Тесты
def test_create_article(client):
    response = client.post(
        "/api/v1/articles/",
        json={"title": "New Article", "content": "New content", "author": "John Doe"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Article"
    assert data["author"] == "John Doe"
    assert "id" in data
    assert "created_at" in data


def test_get_articles(client, test_article):
    response = client.get("/api/v1/articles/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(article["title"] == "Test Article" for article in data)


def test_get_article(client, test_article):
    article_id = test_article["id"]
    response = client.get(f"/api/v1/articles/{article_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == article_id
    assert data["content"] == "Test content"


def test_update_article(client, test_article):
    article_id = test_article["id"]
    response = client.put(
        f"/api/v1/articles/{article_id}",
        json={"title": "Updated Title", "content": "Updated content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"
    assert data["author"] == "Test Author"


def test_delete_article(client, test_article):
    article_id = test_article["id"]
    # Удаляем статью
    delete_response = client.delete(f"/api/v1/articles/{article_id}")
    assert delete_response.status_code == 200

    # Проверяем, что статья удалена
    get_response = client.get(f"/api/v1/articles/{article_id}")
    assert get_response.status_code == 404


def test_article_not_found(client):
    response = client.get("/api/v1/articles/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Статья с ID 999 не найдена"


# Очистка после всех тестов
@pytest.fixture(scope="module", autouse=True)
def cleanup(db_session):
    yield
    # Удаляем все данные после выполнения всех тестов модуля
    db_session.query(Article).delete()
    db_session.commit()