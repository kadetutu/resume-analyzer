"""JWT authentication middleware"""
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from app.core.security import JWTHandler


security = HTTPBearer()


async def verify_jwt(credentials: HTTPAuthCredentials = None) -> dict:
    """Verify JWT token from Authorization header"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = JWTHandler.verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload
