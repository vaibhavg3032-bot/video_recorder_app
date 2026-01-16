# Mobile Video Recorder - FastAPI Application

A FastAPI-based mobile video recording application with local backup functionality, restructured using MVT (Model-View-Template) architecture.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## ✨ Features

- 📹 **Video Recording**: Record videos using device camera in mobile browsers
- 💾 **Local Storage**: Persistent video storage using IndexedDB
- ☁️ **Cloud Upload**: Upload videos to FastAPI backend
- 🔄 **Failure Recovery**: Videos remain accessible locally even if upload fails
- 🔁 **Retry Mechanism**: Retry failed uploads from local storage
- 🏗️ **MVT Architecture**: Clean separation of Models, Views, and Templates

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenSSL (for HTTPS support - usually pre-installed on Linux/Mac)

## 🚀 Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or if you need to use pip3:

```bash
pip3 install -r requirements.txt
```

**Required packages:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `pydantic-settings` - Settings management
- `python-multipart` - File upload support

### Step 2: Verify Installation

Check that all dependencies are installed:

```bash
python3 -c "import fastapi, uvicorn, pydantic; print('All dependencies installed!')"
```

## 🏃 Running the Application

### Option 1: HTTP Server (Development)

**Using the startup script:**
```bash
./run_server.sh
```

**Or directly with Python:**
```bash
python3 main.py
```

**Or using uvicorn:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Access the application:**
- Local: `http://localhost:8000`
- Network: `http://YOUR_IP_ADDRESS:8000`

> ⚠️ **Note**: Camera access requires HTTPS on mobile devices (except localhost). Use HTTPS server for mobile testing.

### Option 2: HTTPS Server (Recommended for Mobile)

**Step 1: Generate SSL Certificate (one-time setup)**

```bash
./generate_ssl_cert.sh
```

This creates:
- `cert.pem` - SSL certificate
- `key.pem` - Private key

**Step 2: Start HTTPS Server**

```bash
./run_server_https.sh
```

**Or directly:**
```bash
python3 main.py
```
(The script automatically detects SSL certificates and starts HTTPS mode)

**Or using uvicorn:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8443 --ssl-keyfile key.pem --ssl-certfile cert.pem --reload
```

**Access the application:**
- HTTPS: `https://YOUR_IP_ADDRESS:8443`
- Local HTTPS: `https://localhost:8443`

> ⚠️ **Security Warning**: Browsers will show a security warning for self-signed certificates. This is normal - click "Advanced" → "Proceed to site" to continue.

### Finding Your IP Address

**Linux/Mac:**
```bash
hostname -I | awk '{print $1}'
```

**Alternative methods:**
```bash
# Linux
ip -4 addr show | grep inet | grep -v 127.0.0.1

# Mac
ifconfig | grep "inet " | grep -v 127.0.0.1
```

## 📁 Project Structure

```
Web app/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app initialization
│   ├── models/                   # Models (Pydantic schemas)
│   │   ├── __init__.py
│   │   └── video.py              # Video-related models
│   ├── views/                    # Views (API routes/endpoints)
│   │   ├── __init__.py
│   │   ├── video.py              # Video API endpoints
│   │   └── health.py             # Health check endpoints
│   ├── templates/                # Templates (HTML files)
│   │   └── video_recorder.html   # Main HTML template
│   └── core/                     # Core configuration
│       ├── __init__.py
│       ├── config.py             # Application settings
│       └── middleware.py         # Middleware setup
├── main.py                       # Entry point (supports HTTP/HTTPS)
├── requirements.txt              # Python dependencies
├── run_server.sh                 # HTTP server startup script
├── run_server_https.sh           # HTTPS server startup script
├── generate_ssl_cert.sh          # SSL certificate generator
├── README.md                     # This file
├── STRUCTURE.md                  # Detailed architecture documentation
└── uploads/                      # Uploaded videos directory (auto-created)
```

## 🏗️ MVT Architecture

### Models (`app/models/`)
- Define data structures and validation schemas using Pydantic
- `video.py`: Contains `VideoUploadResponse` and `HealthResponse` models

### Views (`app/views/`)
- Define API endpoints and route handlers
- `video.py`: Video upload endpoints
- `health.py`: Health check endpoint

### Templates (`app/templates/`)
- HTML templates for serving frontend
- `video_recorder.html`: Main frontend interface

### Core (`app/core/`)
- Application configuration and middleware
- `config.py`: Settings management
- `middleware.py`: CORS and other middleware setup

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the HTML frontend |
| `POST` | `/api/upload` | Upload video file |
| `POST` | `/api/upload-fail` | Simulated upload failure (for testing) |
| `GET` | `/api/health` | Health check endpoint |

### Example API Usage

**Upload Video:**
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@video.webm"
```

**Health Check:**
```bash
curl http://localhost:8000/api/health
```

## ⚙️ Configuration

Settings can be configured via:

1. **Environment variables** (create a `.env` file):
```env
UPLOAD_DIR=uploads
SIMULATE_FAILURE=false
HOST=0.0.0.0
PORT=8000
HTTPS_PORT=8443
```

2. **Direct modification** in `app/core/config.py`

**Key settings:**
- `upload_dir`: Directory for uploaded videos (default: `uploads/`)
- `simulate_failure`: Enable upload failure simulation (default: `False`)
- `host`: Server host (default: `0.0.0.0`)
- `port`: HTTP port (default: `8000`)
- `https_port`: HTTPS port (default: `8443`)

## 🐛 Troubleshooting

### Camera Not Working

**Most Common Issue: HTTPS Required**
- ❌ `http://` URLs will NOT work for camera access on mobile
- ✅ You MUST use `https://` or `localhost`
- **Solution**: Use `./run_server_https.sh` to start with HTTPS

**Other Checks:**
- Check browser permissions (Settings > Site Permissions > Camera)
- Ensure you're using HTTPS or localhost
- Try a different browser
- Check browser console for detailed error messages
- Ensure camera is not being used by another app

### Can't Access from Mobile

- Check firewall settings
- Ensure both devices are on the same network
- **Use HTTPS server (required for camera):**
  ```bash
  ./run_server_https.sh
  # Access at https://YOUR_IP:8443
  ```

### Videos Not Persisting

- Check browser DevTools > Application > IndexedDB
- Ensure browser supports IndexedDB
- Check available storage space

### Import Errors

If you get import errors, ensure you're running from the project root:

```bash
cd "/home/dell/Documents/Web app"
python3 main.py
```

### Port Already in Use

If port 8000 or 8443 is already in use:

```bash
# Find process using the port
lsof -i :8000
# or
netstat -tulpn | grep 8000

# Kill the process or change port in app/core/config.py
```

## 📱 Mobile Testing

1. **Ensure your mobile device is on the same WiFi network** as your computer
2. **Use HTTPS URL**: `https://YOUR_IP_ADDRESS:8443`
3. Open browser on your mobile device
4. Go to the HTTPS URL
5. **Accept the security warning** (self-signed certificate is safe for testing)
6. Grant camera permissions when prompted

## 🔒 Security Notes

- **HTTPS Required**: Camera access requires HTTPS in production
- **CORS**: Currently allows all origins (restrict in production)
- **File Size**: No size limits enforced (add in production)
- **Authentication**: No auth implemented (add in production)

## 📚 Additional Documentation

- `STRUCTURE.md` - Detailed architecture documentation
- Original documentation files (if present):
  - `QUICKSTART.md` - Quick start guide
  - `README_VIDEO_RECORDER.md` - Detailed feature documentation

## 🆘 Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review browser console for errors
3. Check server logs for backend errors
4. Verify all dependencies are installed correctly

## 📝 License

This is a proof-of-concept application for demonstration purposes.

---

**Happy Coding! 🚀**
