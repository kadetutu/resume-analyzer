"""Main FastAPI application setup"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import create_db_and_tables
from app.api.v1 import auth, resumes, analysis

# Create FastAPI app
app = FastAPI(
    title="Resume Analyzer API",
    description="AI-powered resume analysis against job descriptions",
    version="1.0.0",
    debug=settings.debug,
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, settings.backend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    create_db_and_tables()


# Include routers
app.include_router(auth.router)
app.include_router(resumes.router)
app.include_router(analysis.router)


# Health check endpoint
@app.get("/health")
def health_check() -> dict:
    """Health check endpoint"""
    return {"status": "ok", "version": "1.0.0"}


@app.get("/")
def root() -> dict:
    """Root endpoint"""
    return {
        "message": "Welcome to Resume Analyzer API",
        "docs": "/docs",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
