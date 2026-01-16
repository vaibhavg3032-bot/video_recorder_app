"""
Video-related API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from pathlib import Path
import uuid
import asyncio
from typing import Optional

from app.models.video import VideoUploadResponse
from app.core.config import settings

router = APIRouter(tags=["video"])


@router.post("/upload", response_model=VideoUploadResponse)
async def upload_video(file: UploadFile = File(...)):
    """
    Upload video endpoint
    Can simulate failure for testing purposes
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
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix or ".webm"
        filename = f"{file_id}{file_extension}"
        filepath = settings.upload_dir / filename
        
        # Save file
        with open(filepath, "wb") as f:
            content = await file.read()
            f.write(content)
        
        file_size = len(content)
        
        return VideoUploadResponse(
            success=True,
            message="Video uploaded successfully",
            file_id=file_id,
            filename=filename,
            size=file_size,
            size_mb=round(file_size / (1024 * 1024), 2)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )


@router.post("/upload-fail")
async def upload_fail_simulation(file: UploadFile = File(...)):
    """
    Simulated upload failure endpoint for testing
    Always returns an error to test local persistence
    """
    raise HTTPException(
        status_code=500,
        detail="Simulated upload failure - network error (for testing)"
    )
