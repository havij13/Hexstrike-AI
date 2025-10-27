"""
HexStrike AI - Tools Namespace
Flask-RESTX namespace for security tools endpoints.
"""

from flask_restx import Namespace, Resource
from api.models.tool_models import create_tool_models

# Create namespace
ns = Namespace('tools', description='Security Tools Operations')

# Create models
models = create_tool_models(ns)

# Register models
error_model = models['error']
tool_response_model = models['tool_response']

# Import route handlers (to be implemented)
from .routes import *

__all__ = ['ns']
