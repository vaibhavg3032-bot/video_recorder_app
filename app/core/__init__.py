"""
Core configuration and settings
"""
from .config import settings
from .middleware import setup_middleware

__all__ = ["settings", "setup_middleware"]
