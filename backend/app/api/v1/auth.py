"""Authentication API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import JWTHandler
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(request: UserRegisterRequest, session: Session = Depends(get_session)) -> dict:
    """Register a new user"""
    try:
        user = AuthService.register_user(session, request.email, request.password, request.username)
        tokens = AuthService.create_tokens(user)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(request: UserLoginRequest, session: Session = Depends(get_session)) -> dict:
    """Login user"""
    try:
        user = AuthService.login_user(session, request.email, request.password)
        tokens = AuthService.create_tokens(user)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest, session: Session = Depends(get_session)) -> dict:
    """Refresh access token using refresh token"""
    # Verify refresh token
    payload = JWTHandler.verify_token(request.refresh_token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    try:
        user_id = int(payload.get("sub"))
        user = AuthService.get_user_by_id(session, user_id)
        tokens = AuthService.create_tokens(user)
        return tokens
    except (ValueError, KeyError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserResponse)
def get_current_user(token: str = None, session: Session = Depends(get_session)) -> UserResponse:
    """Get current user profile"""
    # In production, use proper JWT bearer token extraction
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")

    payload = JWTHandler.verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    try:
        user_id = int(payload.get("sub"))
        user = AuthService.get_user_by_id(session, user_id)
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            subscription_tier=user.subscription_tier,
            created_at=user.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/logout")
def logout() -> dict:
    """Logout user (token invalidation handled on frontend)"""
    return {"message": "Logged out successfully"}
