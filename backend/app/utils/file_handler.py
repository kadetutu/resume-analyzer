"""File handling utilities for resume processing"""
import io
import os
import tempfile
from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {str(e)}")


def extract_text_from_docx(file_content: bytes) -> str:
    """Extract text from DOCX file"""
    try:
        doc = Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {str(e)}")


def extract_resume_text(filename: str, file_content: bytes) -> str:
    """Extract text from resume file based on format"""
    file_extension = filename.split(".")[-1].lower()

    if file_extension == "pdf":
        return extract_text_from_pdf(file_content)
    elif file_extension == "docx":
        return extract_text_from_docx(file_content)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def save_resume_file(file_content: bytes, filename: str) -> str:
    """Save resume file to temporary storage"""
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, "wb") as f:
        f.write(file
import io
