import pytest
from datetime import timedelta
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from app.core.security import create_access_token, verify_token
from app.core.config import settings


def test_create_access_token():
    data = {"sub": "dev-user", "email": "dev@local"}
    token = create_access_token(data)

    decoded = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert decoded["sub"] == data["sub"]
    assert decoded["email"] == data["email"]
    assert "exp" in decoded


def test_verify_token_valid():
    payload_data = {"sub": "dev-user", "email": "dev@local"}
    token = create_access_token(payload_data)

    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
    decoded = verify_token(credentials)

    assert decoded["sub"] == "dev-user"
    assert decoded["email"] == "dev@local"


def test_verify_token_invalid_signature():
    # Manually tamper the token
    fake_token = jwt.encode({"sub": "fake"}, "wrongsecret", algorithm=settings.JWT_ALGORITHM)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=fake_token)

    with pytest.raises(HTTPException) as exc_info:
        verify_token(credentials)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"


def test_verify_token_expired():
    # Expire the token in the past
    expired_token = create_access_token({"sub": "expired"}, expires_delta=timedelta(seconds=-1))
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=expired_token)

    with pytest.raises(HTTPException) as exc_info:
        verify_token(credentials)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"
