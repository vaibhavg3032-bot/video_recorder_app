# Test Suite for Video Recorder API

This directory contains comprehensive test cases for the Video Recorder API.

## Test Structure

- `conftest.py` - Pytest fixtures and configuration
- `test_video_service.py` - Tests for VideoService class
- `test_video_controller.py` - Tests for VideoController endpoints
- `test_health_controller.py` - Tests for HealthController endpoints
- `test_models.py` - Tests for Pydantic models
- `test_integration.py` - Integration tests

## Running Tests

### Install Dependencies

First, make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_video_service.py
pytest tests/test_video_controller.py
pytest tests/test_health_controller.py
pytest tests/test_models.py
pytest tests/test_integration.py
```

### Run Specific Test Class

```bash
pytest tests/test_video_service.py::TestVideoService
```

### Run Specific Test Method

```bash
pytest tests/test_video_service.py::TestVideoService::test_save_video_success
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

## Test Coverage

The test suite covers:

- ✅ VideoService methods (save, get_path, file_exists, size calculation)
- ✅ VideoController endpoints (upload, upload-fail)
- ✅ HealthController endpoints (health check)
- ✅ Pydantic models validation
- ✅ Integration tests for full API flow
- ✅ Error handling and edge cases
- ✅ File operations and storage
- ✅ Response model validation

## Fixtures

The `conftest.py` file provides the following fixtures:

- `temp_upload_dir` - Temporary directory for test uploads
- `video_service` - VideoService instance with temp directory
- `test_client` - FastAPI TestClient
- `sample_video_file` - Sample video file for testing
- `mock_upload_file` - Mock UploadFile object
- `large_video_file` - Larger video file (1MB) for testing
