"""Resume service for file handling and storage"""
from sqlmodel import Session, select
from app.models.resume import Resume
from app.utils.file_handler import extract_resume_text, save_resume_file
from app.utils.validators import validate_resume_file
from datetime import datetime
import uuid


class ResumeService:
    """Handle resume operations"""

    @staticmethod
    def upload_resume(
        session: Session, user_id: int, filename: str, file_content: bytes
    ) -> Resume:
        """Upload a new resume"""
        # Validate file
        is_valid, message = validate_resume_file(filename, len(file_content))
        if not is_valid:
            raise ValueError(message)

        # Extract text from resume
        try:
            content_text = extract_resume_text(filename, file_content)
        except ValueError as e:
            raise ValueError(f"Failed to process resume: {str(e)}")

        # Generate unique file path
        file_id = str(uuid.uuid4())
        file_path = f"resumes/{user_id}/{file_id}_{filename}"

        # Create resume record
        resume = Resume(
            user_id=user_id,
            file_name=filename,
            file_path=file_path,
            file_content=file_content,
            content_text=content_text,
        )
        session.add(resume)
        session.commit()
        session.refresh(resume)
        return resume

    @staticmethod
    def get_user_resumes(session: Session, user_id: int) -> list[Resume]:
        """Get all resumes for a user"""
        resumes = session.exec(select(Resume).where(Resume.user_id == user_id)).all()
        return list(resumes)

    @staticmethod
    def get_resume_by_id(session: Session, resume_id: int, user_id: int) -> Resume:
        """Get a specific resume by ID"""
        resume = session.exec(
            select(Resume).where((Resume.id == resume_id) & (Resume.user_id == user_id))
        ).first()
        if not resume:
            raise ValueError("Resume not found")
        return resume

    @staticmethod
    def delete_resume(session: Session, resume_id: int, user_id: int) -> bool:
        """Delete a resume"""
        resume = session.exec(
            select(Resume).where((Resume.id == resume_id) & (Resume.user_id == user_id))
        ).first()
        if not resume:
            raise ValueError("Resume not found")

        session.delete(resume)
        session.commit()
        return True
