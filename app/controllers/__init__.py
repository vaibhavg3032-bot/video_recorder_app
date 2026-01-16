"""
Controllers (API Routes) for the Video Recorder API
"""
from fastapi import APIRouter
from .video_controller import VideoController
from .health_controller import HealthController

# Create main API router
api_router = APIRouter(prefix="/api")

# Initialize controllers and get their routers
video_controller = VideoController()
health_controller = HealthController()

# Include sub-routers
api_router.include_router(video_controller.router)
api_router.include_router(health_controller.router)

__all__ = ["api_router", "VideoController", "HealthController"]
