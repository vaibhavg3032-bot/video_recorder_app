"""
Pytest configuration and fixtures
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from io import BytesIO

from app.main import app
from app.services import VideoService


@pytest.fixture
def temp_upload_dir():
    """Create a temporary directory for test uploads"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def video_service(temp_upload_dir):
    """Create a VideoService instance with temporary upload directory"""
    return VideoService(upload_dir=temp_upload_dir)


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def sample_video_file():
    """Return an open file object for the sample video file `sample_video.mp4`.

    This fixture expects a file named `sample_video.mp4` to be present in the
    `tests/` directory. The file is opened in binary mode and yielded so tests
    can read/seek it as needed. The file is closed after the test.
    """
    sample_path = Path(__file__).parent / "sample_video.mp4"
    # Open the real sample file from the tests directory
    fh = open(sample_path, "rb")
    try:
        yield fh
    finally:
        fh.close()


@pytest.fixture
def mock_upload_file(sample_video_file):
    """Create a mock UploadFile for testing"""
    from fastapi import UploadFile
    
    # Read the bytes from the sample file and rewind so callers can re-read it
    file_content = sample_video_file.read()
    sample_video_file.seek(0)

    # Keep the original test filename so saved files preserve the expected extension
    upload_file = UploadFile(
        filename="test_video.webm",
        file=BytesIO(file_content)
    )
    return upload_file


@pytest.fixture
def large_video_file():
    """Create a larger video file for testing (1MB)"""
    content = b"x" * (1024 * 1024)  # 1MB
    file = BytesIO(content)
    file.name = "large_video.webm"
    return file
