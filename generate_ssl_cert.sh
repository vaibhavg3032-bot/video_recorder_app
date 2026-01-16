#!/bin/bash

# Generate self-signed SSL certificate for HTTPS

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Generating self-signed SSL certificate..."

# Generate private key
openssl genrsa -out key.pem 2048

# Generate certificate
openssl req -new -x509 -key key.pem -out cert.pem -days 365 -subj "/CN=localhost"

echo ""
echo "✅ SSL certificate generated successfully!"
echo "   - key.pem (private key)"
echo "   - cert.pem (certificate)"
echo ""
echo "⚠️  Note: Browsers will show a security warning for self-signed certificates."
echo "   This is normal - click 'Advanced' and 'Proceed' to continue."
