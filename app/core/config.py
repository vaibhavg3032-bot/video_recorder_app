"""
Application configuration
"""
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "Mobile Video Recorder POC"
    upload_dir: Path = Path("uploads")
    simulate_failure: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    https_port: int = 8443
    ssl_cert_path: Path = Path("cert.pem")
    ssl_key_path: Path = Path("key.pem")
    reload: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create upload directory if it doesn't exist
        self.upload_dir.mkdir(exist_ok=True)


settings = Settings()
