"""
HexStrike AI - Process Models
API models for process management endpoints.
"""

from flask_restx import fields

def create_process_models(api):
    """Create and return process-related models"""
    
    # Process Info Model
    process_model = api.model('Process', {
        'pid': fields.Integer(description='Process ID'),
        'name': fields.String(description='Process name'),
        'status': fields.String(description='Process status'),
        'started_at': fields.String(description='Start time'),
        'cpu_usage': fields.Float(description='CPU usage percentage'),
        'memory_usage': fields.Float(description='Memory usage percentage')
    })
    
    # Process List Response
    process_list_response = api.model('ProcessList', {
        'success': fields.Boolean(required=True, description='Operation success status'),
        'processes': fields.List(fields.Nested(process_model), description='List of processes'),
        'total': fields.Integer(description='Total number of processes')
    })
    
    return {
        'process': process_model,
        'process_list': process_list_response
    }
