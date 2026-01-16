"""
Main entry point for running the application
Supports both HTTP and HTTPS modes
"""
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from app.core.config import settings

if __name__ == "__main__":
    # Check if running in HTTPS mode
    cert_path = Path(settings.ssl_cert_path)
    key_path = Path(settings.ssl_key_path)
    
    if cert_path.exists() and key_path.exists():
        print("=" * 50)
        print("Starting server with HTTPS (self-signed certificate)")
        print("=" * 50)
        
        # Get IP address
        try:
            ip_address = os.popen('hostname -I').read().split()[0]
            print(f"Access at: https://{ip_address}:{settings.https_port}")
        except:
            print(f"Access at: https://localhost:{settings.https_port}")
        
        print("⚠️  Browser will show security warning - this is normal for self-signed certs")
        print("   Click 'Advanced' → 'Proceed to site' to continue")
        print("=" * 50)
        print("")
        
        uvicorn.run(
            "app.main:app",
            host=settings.host,
            port=settings.https_port,
            ssl_keyfile=str(key_path),
            ssl_certfile=str(cert_path),
            reload=settings.reload
        )
    else:
        print("=" * 50)
        print("Starting server with HTTP")
        print("=" * 50)
        print(f"Access at: http://{settings.host}:{settings.port}")
        print("")
        print("⚠️  For mobile camera access, use HTTPS:")
        print("   1. Run: ./generate_ssl_cert.sh")
        print("   2. Run: ./run_server_https.sh")
        print("=" * 50)
        print("")
        
        uvicorn.run(
            "app.main:app",
            host=settings.host,
            port=settings.port,
            reload=settings.reload
        )
