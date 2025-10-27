"""
HexStrike AI - AI Agent Models
API models for AI agents endpoints.
"""

from flask_restx import fields

def create_ai_models(api):
    """Create and return AI agent-related models"""
    
    # AI Request Model
    ai_request_model = api.model('AIRequest', {
        'prompt': fields.String(required=True, description='User prompt'),
        'agent_type': fields.String(description='AI agent type'),
        'context': fields.Raw(description='Additional context'),
        'options': fields.Raw(description='AI-specific options')
    })
    
    # AI Response Model
    ai_response_model = api.model('AIResponse', {
        'success': fields.Boolean(required=True, description='Operation success status'),
        'response': fields.String(description='AI response'),
        'agent': fields.String(description='Agent used'),
        'timestamp': fields.String(description='Response timestamp'),
        'metadata': fields.Raw(description='Additional metadata')
    })
    
    return {
        'ai_request': ai_request_model,
        'ai_response': ai_response_model
    }
