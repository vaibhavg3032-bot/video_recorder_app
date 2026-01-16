"""
Views (API Routes) for the Video Recorder API
"""
from fastapi import APIRouter
from .video import router as video_router
from .health import router as health_router

# Create main API router
api_router = APIRouter(prefix="/api")

# Include sub-routers
api_router.include_router(video_router)
api_router.include_router(health_router)

__all__ = ["api_router"]
