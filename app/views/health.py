"""
Health check endpoints
"""
from fastapi import APIRouter
from app.models.video import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        message="Video recorder API is running"
    )
