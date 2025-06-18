import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas.blog import BlogPostCreate, BlogPostUpdate, BlogPostOut


# ------------------------
# BlogPostCreate
# ------------------------

def test_blog_post_create_valid():
    data = {"title": "Hello", "content": "World"}
    post = BlogPostCreate(**data)
    assert post.title == "Hello"
    assert post.content == "World"

def test_blog_post_create_missing_title():
    data = {"content": "World"}
    with pytest.raises(ValidationError) as exc_info:
        BlogPostCreate(**data)
    assert "title" in str(exc_info.value)

def test_blog_post_create_missing_content():
    data = {"title": "Hello"}
    with pytest.raises(ValidationError) as exc_info:
        BlogPostCreate(**data)
    assert "content" in str(exc_info.value)


# ------------------------
# BlogPostUpdate
# ------------------------

def test_blog_post_update_all_fields():
    post = BlogPostUpdate(title="New Title", content="Updated content")
    assert post.title == "New Title"
    assert post.content == "Updated content"

def test_blog_post_update_partial():
    post = BlogPostUpdate(title="New Title")
    assert post.title == "New Title"
    assert post.content is None

def test_blog_post_update_empty():
    post = BlogPostUpdate()
    assert post.title is None
    assert post.content is None


# ------------------------
# BlogPostOut
# ------------------------

def test_blog_post_out_valid():
    now = datetime.utcnow()
    post = BlogPostOut(
        id=1,
        title="Final Title",
        content="Final Content",
        created_at=now,
        updated_at=None
    )
    assert post.id == 1
    assert post.created_at == now
    assert post.updated_at is None

def test_blog_post_out_missing_fields():
    data = {
        "id": 1,
        "title": "Oops",
        "content": "Missing time"
        # missing created_at
    }
    with pytest.raises(ValidationError):
        BlogPostOut(**data)
