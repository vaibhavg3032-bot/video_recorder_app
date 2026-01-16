"""
Tests for VideoController
"""
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from io import BytesIO

from app.main import app
from app.core.config import settings


class TestVideoController:
    """Test cases for VideoController"""
    
    def test_upload_video_success(self, test_client, sample_video_file):
        """Test successful video upload"""
        sample_video_file.seek(0)
        response = test_client.post(
            "/api/upload",
            files={"file": ("test_video.webm", sample_video_file, "video/webm")}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert data["message"] == "Video uploaded successfully"
        assert "file_id" in data
        assert "filename" in data
        assert data["filename"].endswith(".webm")
        assert data["size"] > 0
        assert data["size_mb"] >= 0
        assert data["file_id"] in data["filename"]
    
    def test_upload_video_without_file(self, test_client):
        """Test upload endpoint without file returns error"""
        response = test_client.post("/api/upload")
        
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_upload_video_different_formats(self, test_client):
        """Test uploading videos with different file formats"""
        formats = [
            ("test.mp4", "video/mp4"),
            ("test.mov", "video/quicktime"),
            ("test.avi", "video/x-msvideo"),
        ]
        
        for filename, content_type in formats:
            content = b"fake video content"
            response = test_client.post(
                "/api/upload",
                files={"file": (filename, BytesIO(content), content_type)}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["filename"].endswith(Path(filename).suffix)
    
    def test_upload_video_simulated_failure(self, test_client, sample_video_file):
        """Test upload with simulated failure enabled"""
        # Import settings from config (same object used by controller)
        from app.core.config import settings
        
        # Temporarily set simulate_failure to True
        original_value = settings.simulate_failure
        settings.simulate_failure = True
        
        try:
            sample_video_file.seek(0)
            
            response = test_client.post(
                "/api/upload",
                files={"file": ("test_video.webm", sample_video_file, "video/webm")}
            )
            
            assert response.status_code == 500
            data = response.json()
            assert "Simulated upload failure" in data["detail"]
        finally:
            # Restore original value
            settings.simulate_failure = original_value
    
    def test_upload_fail_simulation_endpoint(self, test_client, sample_video_file):
        """Test upload-fail endpoint always returns error"""
        sample_video_file.seek(0)
        response = test_client.post(
            "/api/upload-fail",
            files={"file": ("test_video.webm", sample_video_file, "video/webm")}
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "Simulated upload failure" in data["detail"]
        assert "for testing" in data["detail"]
    
    def test_upload_video_response_model(self, test_client, sample_video_file):
        """Test upload response matches VideoUploadResponse model"""
        sample_video_file.seek(0)
        response = test_client.post(
            "/api/upload",
            files={"file": ("test_video.webm", sample_video_file, "video/webm")}
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields
        required_fields = ["success", "message", "file_id", "filename", "size", "size_mb"]
        for field in required_fields:
            assert field in data
        
        # Verify field types
        assert isinstance(data["success"], bool)
        assert isinstance(data["message"], str)
        assert isinstance(data["file_id"], str)
        assert isinstance(data["filename"], str)
        assert isinstance(data["size"], int)
        assert isinstance(data["size_mb"], (int, float))
    
    def test_upload_video_size_calculation(self, test_client):
        """Test that file size is calculated correctly"""
        # Create a file with known size (1MB)
        content = b"x" * (1024 * 1024)
        response = test_client.post(
            "/api/upload",
            files={"file": ("large_video.webm", BytesIO(content), "video/webm")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["size"] == 1024 * 1024
        assert data["size_mb"] == 1.0
    
    def test_upload_video_methods(self, test_client):
        """Test that upload endpoint only accepts POST"""
        # GET should fail
        response = test_client.get("/api/upload")
        assert response.status_code == 405
        
        # PUT should fail
        response = test_client.put("/api/upload")
        assert response.status_code == 405
    
    @pytest.mark.asyncio
    async def test_upload_video_network_delay(self, test_client, sample_video_file):
        """Test that upload includes network delay simulation"""
        import time
        sample_video_file.seek(0)
        
        start_time = time.time()
        response = test_client.post(
            "/api/upload",
            files={"file": ("test_video.webm", sample_video_file, "video/webm")}
        )
        elapsed_time = time.time() - start_time
        
        assert response.status_code == 200
        # Should have some delay (at least 0.4 seconds due to asyncio.sleep(0.5))
        # Note: TestClient may not perfectly simulate async delays
        assert elapsed_time >= 0.3  # Allow some margin for test execution
