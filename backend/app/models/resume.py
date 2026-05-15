"""Resume model for database"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Resume(SQLModel, table=True):
    """Resume model storing file information and extracted content"""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    file_name: str
    file_path: str
    file_content: bytes  # Binary file content
    content_text: Optional[str] = None  # Extracted resume text
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Resume(id={self.id}, user_id={self.user_id}, file_name={self.file_name})>"
