
from datetime import datetime
import pytest
from app.schemas.blog import BlogPostCreate, BlogPostOut


def test_create_blog_post(client, mocker):
    post_in = BlogPostCreate(title="Mocked Title", content="Mocked Content")
    post_out = BlogPostOut(
        id=1,
        title=post_in.title,
        content=post_in.content,
        created_at=datetime(2024, 1, 1, 0, 0),
        updated_at=None
    )

    mocker.patch("app.api.v1.endpoints.blog.create_post", return_value=post_out)

    response = client.post("/api/v1/blog/posts/", json=post_in.dict())
    assert response.status_code == 200
    assert response.json()["title"] == post_in.title


def test_read_posts(client, mocker):
    mock_post = BlogPostOut(
        id=1,
        title="Title",
        content="Content",
        created_at=datetime(2024, 1, 1, 0, 0),
        updated_at=None
    )
    mocker.patch("app.api.v1.endpoints.blog.get_all_posts", return_value=[mock_post])

    response = client.get("/api/v1/blog/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["id"] == 1


def test_read_post_found(client, mocker):
    mock_post = BlogPostOut(
        id=1,
        title="Title",
        content="Content",
        created_at=datetime(2024, 1, 1, 0, 0),
        updated_at=None
    )
    mocker.patch("app.api.v1.endpoints.blog.get_post", return_value=mock_post)

    response = client.get("/api/v1/blog/posts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_read_post_not_found(client, mocker):
    mocker.patch("app.api.v1.endpoints.blog.get_post", return_value=None)

    response = client.get("/api/v1/blog/posts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_update_post_found(client, mocker):
    updated = BlogPostOut(
        id=1,
        title="Updated",
        content="Updated content",
        created_at=datetime(2024, 1, 1, 0, 0),
        updated_at=datetime(2024, 1, 2, 0, 0)
    )
    mocker.patch("app.api.v1.endpoints.blog.update_post", return_value=updated)

    response = client.put("/api/v1/blog/posts/1", json={"title": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_update_post_not_found(client, mocker):
    mocker.patch("app.api.v1.endpoints.blog.update_post", return_value=None)

    response = client.put("/api/v1/blog/posts/999", json={"title": "Not Found"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_delete_post_found(client, mocker):
    mocker.patch("app.api.v1.endpoints.blog.delete_post", return_value=True)

    response = client.delete("/api/v1/blog/posts/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Post deleted successfully"


def test_delete_post_not_found(client, mocker):
    mocker.patch("app.api.v1.endpoints.blog.delete_post", return_value=False)

    response = client.delete("/api/v1/blog/posts/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"
