"""Pydantic schemas for resume requests and responses"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ResumeUploadRequest(BaseModel):
    """Resume upload request schema"""

    file_name: str
    file_content: bytes


class ResumeResponse(BaseModel):
    """Resume response schema"""

    id: int
    user_id: int
    file_name: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class ResumeDetailResponse(BaseModel):
    """Detailed resume response schema"""

    id: int
    user_id: int
    file_name: str
    file_path: str
    content_text: Optional[str]
    uploaded_at: datetime

    class Config:
        from_attributes = True
