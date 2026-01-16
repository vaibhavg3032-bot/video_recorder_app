"""
Video Controller - Handles video-related API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
import asyncio
from app.models.video import VideoUploadResponse
from app.core.config import settings
from app.services import VideoService


class VideoController:
    """Controller class for video-related endpoints"""
    
    def __init__(self):
        """Initialize VideoController with router and service"""
        self.router = APIRouter(tags=["video"])
        self.video_service = VideoService()
        self._register_routes()
    
    def _register_routes(self):
        """Register all video-related routes"""
        self.router.add_api_route(
            "/upload",
            self.upload_video,
            methods=["POST"],
            response_model=VideoUploadResponse
        )
        self.router.add_api_route(
            "/upload-fail",
            self.upload_fail_simulation,
            methods=["POST"]
        )
    
    async def upload_video(self, file: UploadFile = File(...)) -> VideoUploadResponse:
        """
        Upload video endpoint
        Can simulate failure for testing purposes
        
        Args:
            file: Uploaded video file
            
        Returns:
            VideoUploadResponse with upload details
            
        Raises:
            HTTPException: If upload fails or simulation is enabled
        """
        try:
            # Simulate network delay
            await asyncio.sleep(0.5)
            
            # Simulate failure if enabled
            if settings.simulate_failure:
                raise HTTPException(
                    status_code=500,
                    detail="Simulated upload failure - network error"
                )
            
            # Use service to save video
            file_id, filename, file_size = await self.video_service.save_video(file)
            
            return VideoUploadResponse(
                success=True,
                message="Video uploaded successfully",
                file_id=file_id,
                filename=filename,
                size=file_size,
                size_mb=self.video_service.calculate_size_mb(file_size)
            )
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Upload failed: {str(e)}"
            )
    
    async def upload_fail_simulation(self, file: UploadFile = File(...)):
        """
        Simulated upload failure endpoint for testing
        Always returns an error to test local persistence
        
        Args:
            file: Uploaded video file (not used, for testing only)
            
        Raises:
            HTTPException: Always raises 500 error
        """
        raise HTTPException(
            status_code=500,
            detail="Simulated upload failure - network error (for testing)"
        )
