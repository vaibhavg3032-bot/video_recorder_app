"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from app.core.config import settings
from app.core.middleware import setup_middleware
from app.controllers import api_router

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Mobile Video Recorder POC with Local Backup",
    version="1.0.0"
)

# Setup middleware
setup_middleware(app)

# Include API routes
app.include_router(api_router)

# Root endpoint (serves HTML)
from fastapi.responses import HTMLResponse
from pathlib import Path

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    """Serve the main HTML page"""
    html_path = Path(__file__).parent / "templates" / "video_recorder.html"
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="""
    <html>
        <body>
            <h1>Video Recorder API</h1>
            <p>Please ensure video_recorder.html exists in the templates directory.</p>
        </body>
    </html>
    """)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )
