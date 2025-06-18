from fastapi import FastAPI
from app.api.v1.endpoints import blog, auth
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI with SQLite")

app.include_router(blog.router, prefix="/api/v1/blog", tags=["Blog"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
