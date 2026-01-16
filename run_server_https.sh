#!/bin/bash

# Start FastAPI server with HTTPS (self-signed certificate)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if certificates exist
if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
    echo "=========================================="
    echo "SSL certificates not found!"
    echo "=========================================="
    echo ""
    echo "Generating self-signed SSL certificate..."
    echo ""
    
    ./generate_ssl_cert.sh
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Failed to generate certificates"
        echo "Make sure openssl is installed: sudo apt install openssl"
        exit 1
    fi
fi

echo ""
echo "=========================================="
echo "Mobile Video Recorder - HTTPS Server"
echo "=========================================="
echo ""
echo "Starting FastAPI server with HTTPS..."
echo ""

# Get IP address
IP_ADDRESS=$(hostname -I | awk '{print $1}')

echo "Access the app at:"
echo "  - HTTPS: https://$IP_ADDRESS:8443"
echo "  - HTTPS: https://localhost:8443 (same computer)"
echo ""
echo "📱 For Mobile Device:"
echo "   1. Open browser on your phone"
echo "   2. Go to: https://$IP_ADDRESS:8443"
echo "   3. Accept security warning (self-signed cert is safe)"
echo "   4. Grant camera permissions"
echo ""
echo "⚠️  IMPORTANT:"
echo "   - Browser will show a security warning (this is normal)"
echo "   - Click 'Advanced' → 'Proceed to site' to continue"
echo "   - On mobile: Tap 'Advanced' → 'Proceed to [site]'"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python3 main.py
