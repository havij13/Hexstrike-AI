"""
HexStrike AI - AI Agents Namespace
Flask-RESTX namespace for AI agents endpoints.
"""

from flask_restx import Namespace
from api.models.ai_models import create_ai_models

# Create namespace
ns = Namespace('ai', description='AI Agents Operations')

# Create models
models = create_ai_models(ns)

__all__ = ['ns']
