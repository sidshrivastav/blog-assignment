from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.blog import BlogPostOut, BlogPostCreate, BlogPostUpdate
from app.crud.blog import create_post, get_all_posts, get_post, update_post, delete_post
from app.db.session import get_db
from app.core.security import verify_token

router = APIRouter()

@router.post("/posts/", response_model=BlogPostOut)
def create_blog_post(post: BlogPostCreate, db: Session = Depends(get_db), user_data=Depends(verify_token)):
    return create_post(db, post)

@router.get("/posts/", response_model=list[BlogPostOut])
def read_posts(db: Session = Depends(get_db), user_data=Depends(verify_token)):
    return get_all_posts(db)

@router.get("/posts/{post_id}", response_model=BlogPostOut)
def read_post(post_id: int, db: Session = Depends(get_db), user_data=Depends(verify_token)):
    db_post = get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/posts/{post_id}", response_model=BlogPostOut)
def update_blog_post(post_id: int, post: BlogPostUpdate, db: Session = Depends(get_db), user_data=Depends(verify_token)):
    db_post = update_post(db, post_id, post)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.delete("/posts/{post_id}")
def delete_blog_post(post_id: int, db: Session = Depends(get_db), user_data=Depends(verify_token)):
    deleted = delete_post(db, post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"detail": "Post deleted successfully"}
