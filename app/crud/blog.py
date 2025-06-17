from sqlalchemy.orm import Session
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from app.models.blog import BlogPost

def create_post(db: Session, post: BlogPostCreate):
    db_post = BlogPost(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db: Session, post_id: int):
    return db.query(BlogPost).filter(BlogPost.id == post_id).first()

def get_all_posts(db: Session):
    return db.query(BlogPost).all()

def update_post(db: Session, post_id: int, post: BlogPostUpdate):
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    for field, value in post.dict(exclude_unset=True).items():
        setattr(db_post, field, value)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if not db_post:
        return False
    db.delete(db_post)
    db.commit()
    return True
