"""AI service for resume analysis using OpenAI"""
from app.core.config import settings
import openai
import json


class AIService:
    """Handle AI-powered resume analysis"""

    def __init__(self):
        """Initialize OpenAI client"""
        openai.api_key = settings.openai_api_key

    def analyze_resume(self, resume_text: str, job_description: str) -> dict:
        """Analyze resume against job description using OpenAI"""
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")

        prompt = self._build_prompt(resume_text, job_description)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000,
            )

            content = response.choices[0].message.content
            result = self._parse_response(content)
            return result
        except Exception as e:
            raise ValueError(f"Error analyzing resume: {str(e)}")

    @staticmethod
    def _build_prompt(resume_text: str, job_description: str) -> str:
        """Build prompt for OpenAI"""
        prompt = f"""
You are an expert resume analyst. Analyze the following resume against the job description and provide a detailed assessment.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Please provide your analysis in the following JSON format:
{{
    "match_score": <0-100>,
    "matched_keywords": ["keyword1", "keyword2", ...],
    "missing_keywords": ["keyword1", "keyword2", ...],
    "recommendations": ["recommendation1", "recommendation2", ...]
}}

Focus on:
1. Match score based on keyword overlap and skill matching
2. Keywords from job description found in resume
3. Important keywords from job description missing in resume
4. Specific recommendations to improve match

Respond ONLY with valid JSON, no additional text.
"""
        return prompt.strip()

    @staticmethod
    def _parse_response(content: str) -> dict:
        """Parse OpenAI response"""
        try:
            # Try to extract JSON from response
            result = json.loads(content)
            return {
                "match_score": float(result.get("match_score", 0)),
                "matched_keywords": result.get("matched_keywords", []),
                "missing_keywords": result.get("missing_keywords", []),
                "recommendations": result.get("recommendations", []),
            }
        except json.JSONDecodeError:
            raise ValueError("Failed to parse AI response")
