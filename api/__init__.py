"""
API Module

This module contains the REST API layer for the HexStrike AI system.
"""

from .routes import create_blueprints
from .middleware import setup_middleware
from .models import *

__all__ = [
    'create_blueprints',
    'setup_middleware'
]
