import pytest

from app import schemas
from fastapi import status


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_list = list(map(validate, res.json()))
    print(posts_list)
    assert len(res.json()) == len(test_posts)
    assert res.status_code == status.HTTP_200_OK


@pytest.mark.usefixtures("test_posts")
def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.usefixtures("test_posts")
def test_get_one_post_not_exists(authorized_client):
    res = authorized_client.get("/posts/888888")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.post.id == test_posts[0].id
    assert post.post.content == test_posts[0].content
    assert post.post.title == test_posts[0].title


@pytest.mark.usefixtures("test_posts")
@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "I love peperoni", True),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": title,
            "content": content,
            "published": published
        }
    )

    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


@pytest.mark.usefixtures("test_posts")
@pytest.mark.parametrize("title, content", [("arbitrary title", "aasdfjasdf")])
def test_create_post_default_publish_true(authorized_client, test_user, title,
                                          content):
    res = authorized_client.post(
        "/posts/",
        json={
            "title": title,
            "content": content
        }
    )

    created_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published is True
    assert created_post.owner_id == test_user["id"]


@pytest.mark.usefixtures("test_posts")
@pytest.mark.parametrize("title, content", [("arbitrary title", "aasdfjasdf")])
def test_unauthorized_user_create_post(client, title, content):
    res = client.post("/posts/", json={"title": title, "content": content})
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.usefixtures("test_user")
def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.usefixtures("test_posts", "test_user")
def test_delete_post_non_exists(authorized_client):
    res = authorized_client.delete("/posts/800000000")
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.usefixtures("test_user")
def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.usefixtures("test_user")
def test_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**res.json())
    assert res.status_code == status.HTTP_200_OK
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.id == data['id']


@pytest.mark.usefixtures("test_user")
def test_unauthorized_user_update_post(authorized_client, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.usefixtures("test_posts", "test_user")
def test_update_post_non_exists(authorized_client):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": 800000000
    }
    res = authorized_client.put("/posts/800000000", json=data)
    assert res.status_code == status.HTTP_404_NOT_FOUND
