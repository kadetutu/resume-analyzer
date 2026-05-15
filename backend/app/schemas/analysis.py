"""Pydantic schemas for analysis requests and responses"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AnalysisRequest(BaseModel):
    """Analysis request schema"""

    resume_id: int
    job_description: str


class AnalysisResponse(BaseModel):
    """Analysis response schema"""

    id: int
    user_id: int
    resume_id: int
    match_score: float
    matched_keywords: list
    missing_keywords: list
    recommendations: list
    analyzed_at: datetime

    class Config:
        from_attributes = True
