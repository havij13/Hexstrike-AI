"""
HexStrike AI - API Blueprints
Contains all Flask-RESTX blueprints organized by functionality.
"""

from flask import Blueprint
from flask_restx import Api

# Create main API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Create Flask-RESTX Api instance for Swagger
api = Api(
    api_bp,
    version='1.0',
    title='HexStrike AI API',
    description='Advanced Penetration Testing Framework API with 150+ Security Tools and 12+ AI Agents',
    doc='/docs/',
    prefix='/v1'
)

# Import and register namespaces
from .tools import ns as tools_ns
from .ai_agents import ns as ai_ns
from .processes import ns as processes_ns

api.add_namespace(tools_ns)
api.add_namespace(ai_ns)
api.add_namespace(processes_ns)
