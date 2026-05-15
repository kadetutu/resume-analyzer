"""Input validators for API requests"""
import re
from app.core.config import settings


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"


def validate_resume_file(filename: str, file_size: int) -> tuple[bool, str]:
    """Validate resume file format and size"""
    # Check file size
    if file_size > settings.max_resume_file_size:
        return False, f"File size exceeds {settings.max_resume_file_size / 1024 / 1024}MB limit"

    # Check file format
    allowed_formats = settings.get_allowed_formats()
    file_extension = filename.split(".")[-1].lower()
    if file_extension not in allowed_formats:
        return (
            False,
            f"File format not allowed. Supported formats: {', '.join(allowed_formats)}",
        )

    return True, "File is valid"


def validate_job_description(job_description: str) -> tuple[bool, str]:
    """Validate job description"""
    if not job_description or len(job_description.strip()) < 10:
        return False, "Job description must be at least 10 characters"
    return True, "Job description is valid"
