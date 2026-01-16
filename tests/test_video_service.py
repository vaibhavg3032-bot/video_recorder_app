"""
Tests for VideoService
"""
import pytest
from pathlib import Path
from fastapi import UploadFile
from io import BytesIO

from app.services import VideoService


class TestVideoService:
    """Test cases for VideoService class"""
    
    def test_init_with_default_dir(self, temp_upload_dir):
        """Test VideoService initialization with default directory"""
        service = VideoService(upload_dir=temp_upload_dir)
        assert service.upload_dir == temp_upload_dir
        assert service.upload_dir.exists()
    
    def test_init_creates_directory(self, temp_upload_dir):
        """Test that VideoService creates upload directory if it doesn't exist"""
        new_dir = temp_upload_dir / "new_upload_dir"
        service = VideoService(upload_dir=new_dir)
        assert new_dir.exists()
    
    @pytest.mark.asyncio
    async def test_save_video_success(self, video_service, mock_upload_file):
        """Test successful video save"""
        file_id, filename, file_size = await video_service.save_video(mock_upload_file)
        
        assert file_id is not None
        assert filename is not None
        assert file_size > 0
        assert filename.endswith(".webm")
        assert file_id in filename
        
        # Verify file was saved
        file_path = video_service.get_file_path(filename)
        assert file_path.exists()
        assert file_path.stat().st_size == file_size
    
    @pytest.mark.asyncio
    async def test_save_video_without_extension(self, video_service):
        """Test saving video without file extension"""
        content = b"test video content"
        upload_file = UploadFile(
            filename="test_video",
            file=BytesIO(content)
        )
        
        file_id, filename, file_size = await video_service.save_video(upload_file)
        
        assert filename.endswith(".webm")  # Should default to .webm
        assert file_size == len(content)
    
    @pytest.mark.asyncio
    async def test_save_video_different_extensions(self, video_service):
        """Test saving videos with different extensions"""
        extensions = [".mp4", ".mov", ".avi", ".mkv"]
        
        for ext in extensions:
            content = b"test content"
            upload_file = UploadFile(
                filename=f"test_video{ext}",
                file=BytesIO(content)
            )
            
            file_id, filename, file_size = await video_service.save_video(upload_file)
            assert filename.endswith(ext)
    
    @pytest.mark.asyncio
    async def test_save_video_generates_unique_ids(self, video_service, mock_upload_file):
        """Test that each save generates unique file IDs"""
        file_ids = set()
        
        for _ in range(5):
            mock_upload_file.file.seek(0)  # Reset file pointer
            file_id, _, _ = await video_service.save_video(mock_upload_file)
            file_ids.add(file_id)
        
        assert len(file_ids) == 5  # All IDs should be unique
    
    def test_get_file_path(self, video_service):
        """Test getting file path"""
        filename = "test_file.webm"
        file_path = video_service.get_file_path(filename)
        
        assert isinstance(file_path, Path)
        assert file_path.name == filename
        assert file_path.parent == video_service.upload_dir
    
    def test_file_exists_true(self, video_service, temp_upload_dir):
        """Test file_exists returns True for existing file"""
        test_file = temp_upload_dir / "existing_file.webm"
        test_file.write_bytes(b"test content")
        
        assert video_service.file_exists("existing_file.webm") is True
    
    def test_file_exists_false(self, video_service):
        """Test file_exists returns False for non-existing file"""
        assert video_service.file_exists("non_existing_file.webm") is False
    
    def test_calculate_size_mb(self, video_service):
        """Test size calculation in megabytes"""
        # 1 MB = 1024 * 1024 bytes
        size_bytes = 1024 * 1024
        size_mb = video_service.calculate_size_mb(size_bytes)
        
        assert size_mb == 1.0
        
        # 2.5 MB
        size_bytes = 2 * 1024 * 1024 + 512 * 1024
        size_mb = video_service.calculate_size_mb(size_bytes)
        assert size_mb == 2.5
    
    def test_calculate_size_mb_rounding(self, video_service):
        """Test that size calculation rounds to 2 decimal places"""
        # 1.234 MB
        size_bytes = int(1.234 * 1024 * 1024)
        size_mb = video_service.calculate_size_mb(size_bytes)
        
        assert isinstance(size_mb, float)
        assert len(str(size_mb).split('.')[-1]) <= 2  # Max 2 decimal places
    
    @pytest.mark.asyncio
    async def test_save_video_preserves_content(self, video_service, mock_upload_file):
        """Test that saved file content matches original"""
        original_content = await mock_upload_file.read()
        mock_upload_file.file.seek(0)
        
        file_id, filename, _ = await video_service.save_video(mock_upload_file)
        
        saved_file_path = video_service.get_file_path(filename)
        saved_content = saved_file_path.read_bytes()
        
        assert saved_content == original_content
