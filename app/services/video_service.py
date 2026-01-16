"""
Video service for handling video upload operations
"""
from pathlib import Path
import uuid
from typing import Tuple
from fastapi import UploadFile
from app.core.config import settings


class VideoService:
    """Service class for video-related operations"""
    
    def __init__(self, upload_dir: Path = None):
        """
        Initialize VideoService
        
        Args:
            upload_dir: Directory for storing uploaded videos. 
                       Defaults to settings.upload_dir
        """
        self.upload_dir = upload_dir or settings.upload_dir
        # Ensure upload directory exists
        self.upload_dir.mkdir(exist_ok=True)
    
    async def save_video(self, file: UploadFile) -> Tuple[str, str, int]:
        """
        Save uploaded video file to disk
        
        Args:
            file: FastAPI UploadFile object
            
        Returns:
            Tuple of (file_id, filename, file_size)
            
        Raises:
            Exception: If file saving fails
        """
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix or ".webm"
        filename = f"{file_id}{file_extension}"
        filepath = self.upload_dir / filename
        
        # Save file
        content = await file.read()
        with open(filepath, "wb") as f:
            f.write(content)
        
        file_size = len(content)
        return file_id, filename, file_size
    
    def get_file_path(self, filename: str) -> Path:
        """
        Get full path for a video file
        
        Args:
            filename: Name of the file
            
        Returns:
            Path object for the file
        """
        return self.upload_dir / filename
    
    def file_exists(self, filename: str) -> bool:
        """
        Check if a video file exists
        
        Args:
            filename: Name of the file to check
            
        Returns:
            True if file exists, False otherwise
        """
        return (self.upload_dir / filename).exists()
    
    def calculate_size_mb(self, size_bytes: int) -> float:
        """
        Convert file size from bytes to megabytes
        
        Args:
            size_bytes: File size in bytes
            
        Returns:
            File size in megabytes (rounded to 2 decimal places)
        """
        return round(size_bytes / (1024 * 1024), 2)
