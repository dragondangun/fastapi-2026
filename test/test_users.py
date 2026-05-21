import jwt
import pytest

from app import schemas
from app.config import settings
from fastapi import status


def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello World!!!"
    assert res.status_code == status.HTTP_200_OK


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com",
                                       "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == status.HTTP_201_CREATED


def test_login(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'],
                        "password": test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", status.HTTP_403_FORBIDDEN),
    ("hello123@gmail.com", "wrongpassword", status.HTTP_403_FORBIDDEN),
    ("wrongemail@gmail.com", "wrongpassword", status.HTTP_403_FORBIDDEN),
    (None, "wrongpassword", status.HTTP_422_UNPROCESSABLE_CONTENT),
    ("hello123@gmail.com", None, status.HTTP_422_UNPROCESSABLE_CONTENT),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"
