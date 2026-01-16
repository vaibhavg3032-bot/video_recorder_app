"""
Tests for HealthController
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


class TestHealthController:
    """Test cases for HealthController"""
    
    def test_health_check_endpoint(self, test_client):
        """Test health check endpoint returns correct response"""
        response = test_client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "Video recorder API is running"
    
    def test_health_check_response_model(self, test_client):
        """Test health check response matches model"""
        response = test_client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all required fields are present
        assert "status" in data
        assert "message" in data
        assert isinstance(data["status"], str)
        assert isinstance(data["message"], str)
    
    def test_health_check_method(self, test_client):
        """Test that health check only accepts GET method"""
        # POST should fail
        response = test_client.post("/api/health")
        assert response.status_code == 405  # Method Not Allowed
        
        # PUT should fail
        response = test_client.put("/api/health")
        assert response.status_code == 405
        
        # DELETE should fail
        response = test_client.delete("/api/health")
        assert response.status_code == 405
