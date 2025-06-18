import pytest

def test_login_dev_user(client):
    response = client.post("/api/v1/auth/login")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["access_token"], str)
