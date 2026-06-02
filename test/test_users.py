import jwt
import pytest

from app import schemas
from app.config import settings
from fastapi import status


def test_root(client):
    res = client.get("/")
    assert res.status_code == status.HTTP_200_OK

    assert res.json().get("message") == "Hello World!!!"


def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com",
                                       "password": "password123"})

    assert res.status_code == status.HTTP_201_CREATED

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"


def test_login(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'],
                        "password": test_user['password']}
    )

    assert res.status_code == status.HTTP_200_OK

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"


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


def test_create_user_duplicate_email(client, test_user):
    res = client.post("/users/", json={"email": test_user["email"],
                                       "password": "another_password"})

    assert res.status_code == status.HTTP_409_CONFLICT
    assert res.json()["detail"] == "User with this email already exists"
