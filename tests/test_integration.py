"""
Integration tests for the Video Recorder API
"""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import os

from app.main import app


class TestIntegration:
    """Integration test cases"""
    
    def test_full_upload_flow(self, test_client, sample_video_file):
        """Test complete video upload flow"""
        # Upload video
        sample_video_file.seek(0)
        response = test_client.post(
            "/api/upload",
            files={"file": ("test_video.webm", sample_video_file, "video/webm")}
        )
        
        assert response.status_code == 200
        data = response.json()
        filename = data["filename"]
        
        # Verify file exists on disk
        upload_dir = Path("uploads")
        file_path = upload_dir / filename
        assert file_path.exists()
        assert file_path.stat().st_size == data["size"]
        
        # Cleanup
        if file_path.exists():
            file_path.unlink()
    
    def test_health_check_after_upload(self, test_client, sample_video_file):
        """Test that health check still works after upload"""
        # Upload a video
        sample_video_file.seek(0)
        upload_response = test_client.post(
            "/api/upload",
            files={"file": ("test_video.webm", sample_video_file, "video/webm")}
        )
        assert upload_response.status_code == 200
        
        # Check health
        health_response = test_client.get("/api/health")
        assert health_response.status_code == 200
        assert health_response.json()["status"] == "ok"
    
    def test_multiple_uploads(self, test_client):
        """Test multiple consecutive uploads"""
        upload_count = 3
        file_ids = []
        
        for i in range(upload_count):
            content = f"test video content {i}".encode()
            response = test_client.post(
                "/api/upload",
                files={"file": (f"test_{i}.webm", content, "video/webm")}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            file_ids.append(data["file_id"])
        
        # Verify all file IDs are unique
        assert len(set(file_ids)) == upload_count
    
    def test_api_routes_registered(self, test_client):
        """Test that all API routes are properly registered"""
        # Health endpoint
        response = test_client.get("/api/health")
        assert response.status_code == 200
        
        # Upload endpoint (should fail without file, but endpoint exists)
        response = test_client.post("/api/upload")
        assert response.status_code == 422  # Unprocessable Entity (missing file)
        
        # Upload-fail endpoint
        response = test_client.post("/api/upload-fail")
        assert response.status_code == 422  # Unprocessable Entity (missing file)
    
    def test_root_endpoint(self, test_client):
        """Test root endpoint serves HTML"""
        response = test_client.get("/")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert len(response.text) > 0
    
    def test_api_prefix(self, test_client):
        """Test that API routes use /api prefix"""
        # Health check with prefix
        response = test_client.get("/api/health")
        assert response.status_code == 200
        
        # Health check without prefix should fail
        response = test_client.get("/health")
        assert response.status_code == 404
    
    def test_error_handling(self, test_client):
        """Test error handling across the API"""
        # Test 404 for non-existent endpoint
        response = test_client.get("/api/nonexistent")
        assert response.status_code == 404
        
        # Test 405 for wrong method
        response = test_client.get("/api/upload")
        assert response.status_code == 405
        
        # Test 422 for invalid request
        response = test_client.post("/api/upload", json={"invalid": "data"})
        assert response.status_code == 422
