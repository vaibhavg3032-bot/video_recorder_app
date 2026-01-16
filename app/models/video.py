"""
Video-related Pydantic models
"""
from pydantic import BaseModel, Field
from typing import Optional


class VideoUploadResponse(BaseModel):
    """Response model for video upload"""
    success: bool = Field(..., description="Whether the upload was successful")
    message: str = Field(..., description="Status message")
    file_id: str = Field(..., description="Unique file identifier")
    filename: str = Field(..., description="Generated filename")
    size: int = Field(..., description="File size in bytes")
    size_mb: float = Field(..., description="File size in megabytes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Video uploaded successfully",
                "file_id": "123e4567-e89b-12d3-a456-426614174000",
                "filename": "123e4567-e89b-12d3-a456-426614174000.webm",
                "size": 1048576,
                "size_mb": 1.0
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Status message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "message": "Video recorder API is running"
            }
        }
