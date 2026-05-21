from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.config import settings
from app.database import Base, get_db
from app.main import app
from app.models import Post
from app.oauth2 import create_access_token

from app import schemas

SQLALCHEY_DATABASE_URL = \
    f'postgresql+psycopg://{settings.database_username}:' \
    f'{settings.database_password}@{settings.database_hostname}:' \
    f'{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def user_factory(client):
    def create_user(
        email: str = "hello123@gmail.com",
        password: str = "password123",
    ):
        user_data = {
            "email": email,
            "password": password,
        }

        res = client.post("/users/", json=user_data)

        assert res.status_code == status.HTTP_201_CREATED, res.text

        user = schemas.UserOut(**res.json())

        return {
            "id": user.id,
            "email": user.email,
            "password": password,
        }

    return create_user


@pytest.fixture
def test_user(user_factory):
    return user_factory(
        email="hello123@gmail.com",
        password="password123",
    )


@pytest.fixture
def test_user2(user_factory):
    return user_factory(
        email="hello1234@gmail.com",
        password="password123",
    )


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "4th title",
            "content": "4th content",
            "owner_id": test_user2['id']
        },
    ]

    posts = [Post(**p) for p in posts_data]
    session.add_all(posts)
    session.commit()

    return session.query(Post).all()
