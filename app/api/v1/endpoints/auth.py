from fastapi import APIRouter
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login")
def login_dev_user():
    """Simulate user login and return a JWT."""
    token = create_access_token({"sub": "dev-user", "email": "dev@local"})
    return {"access_token": token, "token_type": "bearer"}
