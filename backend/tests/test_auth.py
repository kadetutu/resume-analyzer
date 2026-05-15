"""Authentication endpoint tests"""
import pytest
from fastapi import status


def test_register_user(client, test_user_data):
    """Test user registration"""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_register_user_duplicate_email(client, test_user_data):
    """Test registration with duplicate email"""
    # Register first user
    client.post("/api/v1/auth/register", json=test_user_data)

    # Try to register with same email
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_user_weak_password(client):
    """Test registration with weak password"""
    data = {
        "email": "test@example.com",
        "password": "weak",
    }
    response = client.post("/api/v1/auth/register", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_user(client, test_user_data, test_login_data):
    """Test user login"""
    # Register user first
    client.post("/api/v1/auth/register", json=test_user_data)

    # Login
    response = client.post("/api/v1/auth/login", json=test_login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_user_invalid_credentials(client):
    """Test login with invalid credentials"""
    data = {
        "email": "nonexistent@example.com",
        "password": "WrongPassword123",
    }
    response = client.post("/api/v1/auth/login", json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout(client):
    """Test user logout"""
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["message"] == "Logged out successfully"
