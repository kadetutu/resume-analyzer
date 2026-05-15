"""Analysis result model for database"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import json


class AnalysisResult(SQLModel, table=True):
    """Analysis result model storing resume-to-job-description matching"""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    resume_id: int = Field(foreign_key="resume.id", index=True)
    job_description: str
    match_score: float  # 0.0 to 100.0
    matched_keywords: str = Field(default="[]")  # JSON array
    missing_keywords: str = Field(default="[]")  # JSON array
    recommendations: str = Field(default="[]")  # JSON array
    analyzed_at: datetime = Field(default_factory=datetime.utcnow)

    def set_matched_keywords(self, keywords: list) -> None:
        """Set matched keywords as JSON"""
        self.matched_keywords = json.dumps(keywords)

    def get_matched_keywords(self) -> list:
        """Get matched keywords from JSON"""
        return json.loads(self.matched_keywords) if self.matched_keywords else []

    def set_missing_keywords(self, keywords: list) -> None:
        """Set missing keywords as JSON"""
        self.missing_keywords = json.dumps(keywords)

    def get_missing_keywords(self) -> list:
        """Get missing keywords from JSON"""
        return json.loads(self.missing_keywords) if self.missing_keywords else []

    def set_recommendations(self, recommendations: list) -> None:
        """Set recommendations as JSON"""
        self.recommendations = json.dumps(recommendations)

    def get_recommendations(self) -> list:
        """Get recommendations from JSON"""
        return json.loads(self.recommendations) if self.recommendations else []

    def __repr__(self) -> str:
        return f"<AnalysisResult(id={self.id}, user_id={self.user_id}, score={self.match_score})>"
