"""
Tests for Pydantic models
"""
import pytest
from pydantic import ValidationError

from app.models.video import VideoUploadResponse, HealthResponse


class TestVideoUploadResponse:
    """Test cases for VideoUploadResponse model"""
    
    def test_valid_response(self):
        """Test creating valid VideoUploadResponse"""
        response = VideoUploadResponse(
            success=True,
            message="Video uploaded successfully",
            file_id="123e4567-e89b-12d3-a456-426614174000",
            filename="123e4567-e89b-12d3-a456-426614174000.webm",
            size=1048576,
            size_mb=1.0
        )
        
        assert response.success is True
        assert response.message == "Video uploaded successfully"
        assert response.file_id == "123e4567-e89b-12d3-a456-426614174000"
        assert response.filename == "123e4567-e89b-12d3-a456-426614174000.webm"
        assert response.size == 1048576
        assert response.size_mb == 1.0
    
    def test_missing_required_fields(self):
        """Test that missing required fields raise ValidationError"""
        with pytest.raises(ValidationError):
            VideoUploadResponse(
                success=True,
                message="Test"
                # Missing other required fields
            )
    
    def test_field_types(self):
        """Test that fields have correct types"""
        response = VideoUploadResponse(
            success=True,
            message="Test",
            file_id="test-id",
            filename="test.webm",
            size=1000,
            size_mb=0.001
        )
        
        assert isinstance(response.success, bool)
        assert isinstance(response.message, str)
        assert isinstance(response.file_id, str)
        assert isinstance(response.filename, str)
        assert isinstance(response.size, int)
        assert isinstance(response.size_mb, float)
    
    def test_json_serialization(self):
        """Test that model can be serialized to JSON"""
        response = VideoUploadResponse(
            success=True,
            message="Test",
            file_id="test-id",
            filename="test.webm",
            size=1000,
            size_mb=0.001
        )
        
        json_data = response.model_dump()
        assert isinstance(json_data, dict)
        assert json_data["success"] is True
        assert json_data["message"] == "Test"
    
    def test_model_validation(self):
        """Test model validation with invalid types"""
        with pytest.raises(ValidationError):
            VideoUploadResponse(
                success="not a boolean",  # Should be bool
                message="Test",
                file_id="test-id",
                filename="test.webm",
                size=1000,
                size_mb=0.001
            )


class TestHealthResponse:
    """Test cases for HealthResponse model"""
    
    def test_valid_response(self):
        """Test creating valid HealthResponse"""
        response = HealthResponse(
            status="ok",
            message="Video recorder API is running"
        )
        
        assert response.status == "ok"
        assert response.message == "Video recorder API is running"
    
    def test_missing_required_fields(self):
        """Test that missing required fields raise ValidationError"""
        with pytest.raises(ValidationError):
            HealthResponse(
                status="ok"
                # Missing message
            )
    
    def test_field_types(self):
        """Test that fields have correct types"""
        response = HealthResponse(
            status="ok",
            message="Test message"
        )
        
        assert isinstance(response.status, str)
        assert isinstance(response.message, str)
    
    def test_json_serialization(self):
        """Test that model can be serialized to JSON"""
        response = HealthResponse(
            status="ok",
            message="Test message"
        )
        
        json_data = response.model_dump()
        assert isinstance(json_data, dict)
        assert json_data["status"] == "ok"
        assert json_data["message"] == "Test message"
    
    def test_different_status_values(self):
        """Test HealthResponse with different status values"""
        statuses = ["ok", "healthy", "running", "up"]
        
        for status in statuses:
            response = HealthResponse(
                status=status,
                message="Test"
            )
            assert response.status == status
