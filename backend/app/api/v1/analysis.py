"""Analysis API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import JWTHandler
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.resume_service import ResumeService
from app.services.ai_service import AIService
from app.services.rate_limit_service import RateLimitService
from app.models.analysis import AnalysisResult
from app.models.user import User
from sqlmodel import select

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])


def get_current_user_id(token: str = None) -> int:
    """Extract user ID from JWT token"""
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")

    payload = JWTHandler.verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    try:
        return int(payload.get("sub"))
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@router.post("/analyze", response_model=AnalysisResponse)
def analyze_resume(
    request: AnalysisRequest, token: str = None, session: Session = Depends(get_session)
) -> AnalysisResponse:
    """Analyze resume against job description"""
    user_id = get_current_user_id(token)

    try:
        # Get user to check subscription tier
        user = session.exec(select(User).where(User.id == user_id)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        # Check rate limit
        can_analyze, message = RateLimitService.check_subscription_limit(
            session, user_id, user.subscription_tier
        )
        if not can_analyze:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=message)

        # Get resume
        resume = ResumeService.get_resume_by_id(session, request.resume_id, user_id)

        # Initialize AI service
        ai_service = AIService()

        # Analyze resume
        analysis_result = ai_service.analyze_resume(resume.content_text, request.job_description)

        # Create analysis record
        analysis = AnalysisResult(
            user_id=user_id,
            resume_id=request.resume_id,
            job_description=request.job_description,
            match_score=analysis_result["match_score"],
        )
        analysis.set_matched_keywords(analysis_result["matched_keywords"])
        analysis.set_missing_keywords(analysis_result["missing_keywords"])
        analysis.set_recommendations(analysis_result["recommendations"])

        session.add(analysis)
        session.commit()

        # Log usage
        RateLimitService.log_analysis_usage(session, user_id)

        session.refresh(analysis)

        return AnalysisResponse(
            id=analysis.id,
            user_id=analysis.user_id,
            resume_id=analysis.resume_id,
            match_score=analysis.match_score,
            matched_keywords=analysis.get_matched_keywords(),
            missing_keywords=analysis.get_missing_keywords(),
            recommendations=analysis.get_recommendations(),
            analyzed_at=analysis.analyzed_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
