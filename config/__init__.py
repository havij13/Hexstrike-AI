"""
Configuration Module

This module contains configuration management for the HexStrike AI application.
"""

from .settings import Config
from .logging import setup_logging

__all__ = ['Config', 'setup_logging']