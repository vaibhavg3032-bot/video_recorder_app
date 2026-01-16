"""
Health Controller - Handles health check API endpoints
"""
from fastapi import APIRouter
from app.models.video import HealthResponse


class HealthController:
    """Controller class for health check endpoints"""
    
    def __init__(self):
        """Initialize HealthController with router"""
        self.router = APIRouter(tags=["health"])
        self._register_routes()
    
    def _register_routes(self):
        """Register all health-related routes"""
        self.router.add_api_route(
            "/health",
            self.health_check,
            methods=["GET"],
            response_model=HealthResponse
        )
    
    async def health_check(self) -> HealthResponse:
        """
        Health check endpoint
        
        Returns:
            HealthResponse with API status
        """
        return HealthResponse(
            status="ok",
            message="Video recorder API is running"
        )
