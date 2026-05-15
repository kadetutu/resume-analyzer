"""Authentication service for user registration and login"""
from sqlmodel import Session, select
from app.models.user import User
from app.core.security import PasswordHandler, JWTHandler
from app.utils.validators import validate_email, validate_password
from datetime import datetime


class AuthService:
    """Handle user authentication operations"""

    @staticmethod
    def register_user(session: Session, email: str, password: str, username: str = None) -> User:
        """Register a new user"""
        # Validate email
        if not validate_email(email):
            raise ValueError("Invalid email format")

        # Validate password strength
        is_valid, message = validate_password(password)
        if not is_valid:
            raise ValueError(message)

        # Check if email already exists
        existing_user = session.exec(select(User).where(User.email == email)).first()
        if existing_user:
            raise ValueError("Email already registered")

        # Check if username already exists (if provided)
        if username:
            existing_username = session.exec(select(User).where(User.username == username)).first()
            if existing_username:
                raise ValueError("Username already taken")

        # Create new user
        user = User(
            email=email,
            username=username,
            password_hash=PasswordHandler.hash_password(password),
            subscription_tier="free",
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def login_user(session: Session, email: str, password: str) -> User:
        """Login user and return user object"""
        # Find user by email
        user = session.exec(select(User).where(User.email == email)).first()
        if not user:
            raise ValueError("Invalid email or password")

        # Verify password
        if not PasswordHandler.verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> User:
        """Get user by ID"""
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise ValueError("User not found")
        return user

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> User:
        """Get user by email"""
        user = session.exec(select(User).where(User.email == email)).first()
        return user

    @staticmethod
    def create_tokens(user: User) -> dict:
        """Create access and refresh tokens for user"""
        data = {"sub": str(user.id), "email": user.email}
        access_token = JWTHandler.create_access_token(data)
        refresh_token = JWTHandler.create_refresh_token(data)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 30,  # minutes
        }
