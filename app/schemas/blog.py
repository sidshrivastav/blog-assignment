from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BlogPostCreate(BaseModel):
    title: str
    content: str

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class BlogPostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
