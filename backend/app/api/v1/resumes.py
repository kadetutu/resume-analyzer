"""Resume API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlmodel import Session
from app.core.database import get_session
from app.core.security import JWTHandler
from app.schemas.resume import ResumeResponse, ResumeDetailResponse
from app.services.resume_service import ResumeService
import io

router = APIRouter(prefix="/api/v1/resumes", tags=["resumes"])


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


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    token: str = None,
    session: Session = Depends(get_session),
) -> ResumeResponse:
    """Upload a resume file"""
    user_id = get_current_user_id(token)

    try:
        # Read file content
        file_content = await file.read()

        # Upload resume
        resume = ResumeService.upload_resume(session, user_id, file.filename, file_content)

        return ResumeResponse(
            id=resume.id,
            user_id=resume.user_id,
            file_name=resume.file_name,
            uploaded_at=resume.uploaded_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=list[ResumeResponse])
def get_resumes(token: str = None, session: Session = Depends(get_session)) -> list[ResumeResponse]:
    """Get all resumes for current user"""
    user_id = get_current_user_id(token)

    try:
        resumes = ResumeService.get_user_resumes(session, user_id)
        return [
            ResumeResponse(
                id=r.id,
                user_id=r.user_id,
                file_name=r.file_name,
                uploaded_at=r.uploaded_at,
            )
            for r in resumes
        ]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{resume_id}", response_model=ResumeDetailResponse)
def get_resume(
    resume_id: int, token: str = None, session: Session = Depends(get_session)
) -> ResumeDetailResponse:
    """Get specific resume details"""
    user_id = get_current_user_id(token)

    try:
        resume = ResumeService.get_resume_by_id(session, resume_id, user_id)
        return ResumeDetailResponse(
            id=resume.id,
            user_id=resume.user_id,
            file_name=resume.file_name,
            file_path=resume.file_path,
            content_text=resume.content_text,
            uploaded_at=resume.uploaded_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{resume_id}")
def delete_resume(resume_id: int, token: str = None, session: Session = Depends(get_session)) -> dict:
    """Delete a resume"""
    user_id = get_current_user_id(token)

    try:
        ResumeService.delete_resume(session, resume_id, user_id)
        return {"message": "Resume deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
