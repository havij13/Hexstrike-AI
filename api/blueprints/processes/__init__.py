"""
HexStrike AI - Processes Namespace
Flask-RESTX namespace for process management endpoints.
"""

from flask_restx import Namespace
from api.models.process_models import create_process_models

# Create namespace
ns = Namespace('processes', description='Process Management Operations')

# Create models
models = create_process_models(ns)

__all__ = ['ns']
