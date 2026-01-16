#!/bin/bash

# Mobile Video Recorder - FastAPI Server Startup Script

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Mobile Video Recorder - POC Server"
echo "=========================================="
echo ""
echo "Starting FastAPI server..."
echo ""
echo "Access the app at:"
echo "  - Local: http://localhost:8000"
echo "  - Network: http://$(hostname -I | awk '{print $1}'):8000"
echo ""
echo "For mobile testing, use the network IP address"
echo "or use the HTTPS server: ./run_server_https.sh"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python3 main.py
