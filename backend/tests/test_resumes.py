"""Resume service tests"""
import pytest
from app.services.resume_service import ResumeService
from app.services.auth_service import AuthService
from app.models.resume import Resume


def test_upload_resume(session, test_user_data):
    """Test resume upload"""
    # Create user
    user = AuthService.register_user(session, test_user_data["email"], test_user_data["password"])

    # Create test file content (simplified PDF bytes)
    test_file_content = b"%PDF-1.4\n%Test PDF content"

    # Upload resume
    resume = ResumeService.upload_resume(
        session, user.id, "test_resume.pdf", test_file_content
    )

    assert resume.user_id == user.id
    assert resume.file_name == "test_resume.pdf"
    assert resume.file_content == test_file_content


def test_get_user_resumes(session, test_user_data):
    """Test getting user's resumes"""
    # Create user
    user = AuthService.register_user(session, test_user_data["email"], test_user_data["password"])

    # Upload resumes
    test_file_content = b"%PDF-1.4\n%Test PDF content"
    resume1 = ResumeService.upload_resume(
        session, user.id, "resume1.pdf", test_file_content
    )
    resume2 = ResumeService.upload_resume(
        session, user.id, "resume2.pdf", test_file_content
    )

    # Get resumes
    resumes = ResumeService.get_user_resumes(session, user.id)
    assert len(resumes) == 2
    assert resume1.id in [r.id for r in resumes]
    assert resume2.id in [r.id for r in resumes]


def test_delete_resume(session, test_user_data):
    """Test resume deletion"""
    # Create user
    user = AuthService.register_user(session, test_user_data["email"], test_user_data["password"])

    # Upload resume
    test_file_content = b"%PDF-1.4\n%Test PDF content"
    resume = ResumeService.upload_resume(
        session, user.id, "test_resume.pdf", test_file_content
    )

    # Delete resume
    result = ResumeService.delete_resume(session, resume.id, user.id)
    assert result is True

    # Verify deletion
    with pytest.raises(ValueError):
        ResumeService.get_resume_by_id(session, resume.id, user.id)
