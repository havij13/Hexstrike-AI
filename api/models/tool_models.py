"""
HexStrike AI - Tool Models
API models for security tools endpoints.
"""

from flask_restx import fields

def create_tool_models(api):
    """Create and return tool-related models"""
    
    # Error Response Model
    error_model = api.model('Error', {
        'success': fields.Boolean(required=True, description='Operation success status'),
        'error': fields.String(required=True, description='Error message'),
        'details': fields.Raw(description='Additional error details')
    })
    
    # Success Response Model
    success_model = api.model('Success', {
        'success': fields.Boolean(required=True, description='Operation success status'),
        'message': fields.String(description='Success message'),
        'data': fields.Raw(description='Response data')
    })
    
    # Tool Request Model
    tool_request_model = api.model('ToolRequest', {
        'target': fields.String(required=True, description='Target URL, IP, or domain'),
        'options': fields.Raw(description='Tool-specific options')
    })
    
    # Nmap Request Model
    nmap_request_model = api.inherit('NmapRequest', tool_request_model, {
        'scan_type': fields.String(description='Scan type (syn, tcp, udp, etc.)'),
        'ports': fields.String(description='Port range (e.g., 1-1000)'),
        'arguments': fields.String(description='Additional Nmap arguments')
    })
    
    # Rustscan Request Model
    rustscan_request_model = api.inherit('RustscanRequest', tool_request_model, {
        'ports': fields.String(description='Port range (e.g., 1-1000)'),
        'scan_type': fields.String(description='Scan type'),
        'timeout': fields.Integer(description='Timeout in seconds')
    })
    
    # Masscan Request Model
    masscan_request_model = api.inherit('MasscanRequest', tool_request_model, {
        'ports': fields.String(description='Port range (e.g., 1-1000)'),
        'rate': fields.Integer(description='Packets per second rate')
    })
    
    # Gobuster Request Model
    gobuster_request_model = api.inherit('GobusterRequest', tool_request_model, {
        'mode': fields.String(description='Mode (dir, dns, fuzz, etc.)'),
        'wordlist': fields.String(description='Wordlist path'),
        'extensions': fields.String(description='File extensions (e.g., php,html)'),
        'threads': fields.Integer(description='Number of threads')
    })
    
    # Nuclei Request Model
    nuclei_request_model = api.inherit('NucleiRequest', tool_request_model, {
        'templates': fields.String(description='Template directory'),
        'tags': fields.String(description='Template tags'),
        'severity': fields.String(description='Severity level'),
        'rate_limit': fields.Integer(description='Rate limit')
    })
    
    # Tool Response Model
    tool_response_model = api.model('ToolResponse', {
        'success': fields.Boolean(required=True, description='Operation success status'),
        'tool': fields.String(description='Tool name'),
        'target': fields.String(description='Target'),
        'output': fields.String(description='Tool output'),
        'duration': fields.Float(description='Execution duration in seconds'),
        'timestamp': fields.String(description='Execution timestamp'),
        'metadata': fields.Raw(description='Additional metadata')
    })
    
    return {
        'error': error_model,
        'success': success_model,
        'tool_request': tool_request_model,
        'nmap_request': nmap_request_model,
        'rustscan_request': rustscan_request_model,
        'masscan_request': masscan_request_model,
        'gobuster_request': gobuster_request_model,
        'nuclei_request': nuclei_request_model,
        'tool_response': tool_response_model
    }
