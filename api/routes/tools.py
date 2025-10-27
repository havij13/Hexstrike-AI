"""
Tools Routes

This module handles tool-related API endpoints.
"""

from flask import Blueprint, request, jsonify, current_app
from api.middleware.auth_middleware import require_auth, get_current_user
from tools.tool_registry import tool_registry
import asyncio
import logging

tools_bp = Blueprint('tools', __name__)
logger = logging.getLogger(__name__)


@tools_bp.route('/', methods=['GET'])
@require_auth()
def list_tools():
    """List available tools"""
    try:
        # Initialize tool registry if not already done
        if not tool_registry._initialized:
            tool_registry.initialize()
        
        category = request.args.get('category')
        search = request.args.get('search')
        
        if search:
            tools = tool_registry.search_tools(search)
        elif category:
            tools = tool_registry.get_tools_by_category(category)
        else:
            tools = tool_registry.list_tools()
        
        # Get detailed info for each tool
        tool_details = []
        for tool_name in tools:
            tool_info = tool_registry.get_tool_info(tool_name)
            if tool_info:
                tool_details.append(tool_info)
        
        return jsonify({
            'success': True,
            'tools': tool_details,
            'total': len(tool_details)
        }), 200
        
    except Exception as e:
        logger.error(f"List tools error: {str(e)}")
        return jsonify({'error': 'Failed to list tools'}), 500


@tools_bp.route('/categories', methods=['GET'])
@require_auth()
def list_categories():
    """List tool categories"""
    try:
        if not tool_registry._initialized:
            tool_registry.initialize()
        
        categories = tool_registry.list_categories()
        
        # Get stats for each category
        category_stats = []
        for category in categories:
            tools = tool_registry.get_tools_by_category(category)
            category_stats.append({
                'name': category,
                'tool_count': len(tools),
                'tools': tools
            })
        
        return jsonify({
            'success': True,
            'categories': category_stats,
            'total': len(categories)
        }), 200
        
    except Exception as e:
        logger.error(f"List categories error: {str(e)}")
        return jsonify({'error': 'Failed to list categories'}), 500


@tools_bp.route('/<tool_name>', methods=['GET'])
@require_auth()
def get_tool_info(tool_name):
    """Get detailed information about a specific tool"""
    try:
        if not tool_registry._initialized:
            tool_registry.initialize()
        
        tool_info = tool_registry.get_tool_info(tool_name)
        
        if not tool_info:
            return jsonify({'error': 'Tool not found'}), 404
        
        return jsonify({
            'success': True,
            'tool': tool_info
        }), 200
        
    except Exception as e:
        logger.error(f"Get tool info error: {str(e)}")
        return jsonify({'error': 'Failed to get tool info'}), 500


@tools_bp.route('/<tool_name>/execute', methods=['POST'])
@require_auth()
def execute_tool(tool_name):
    """Execute a specific tool"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        target = data.get('target')
        parameters = data.get('parameters', {})
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Validate parameters
        if not tool_registry.validate_tool_parameters(tool_name, parameters):
            return jsonify({'error': 'Invalid parameters'}), 400
        
        # Create tool instance
        tool = tool_registry.create_tool(tool_name)
        
        if not tool:
            return jsonify({'error': 'Tool not found or not available'}), 404
        
        # Check if tool is available
        if not tool.is_available():
            return jsonify({'error': 'Tool is not available on this system'}), 503
        
        # Execute tool
        logger.info(f"Executing tool {tool_name} against {target} by user {user.get('username')}")
        
        result = asyncio.run(tool.execute(target, parameters))
        
        return jsonify({
            'success': result.success,
            'data': result.data,
            'raw_output': result.raw_output,
            'error_message': result.error_message,
            'execution_time': result.execution_time,
            'command_executed': result.command_executed,
            'exit_code': result.exit_code
        }), 200 if result.success else 500
        
    except Exception as e:
        logger.error(f"Execute tool error: {str(e)}")
        return jsonify({'error': 'Failed to execute tool'}), 500


@tools_bp.route('/<tool_name>/validate', methods=['POST'])
@require_auth()
def validate_tool_parameters(tool_name):
    """Validate tool parameters"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        parameters = data.get('parameters', {})
        
        is_valid = tool_registry.validate_tool_parameters(tool_name, parameters)
        
        return jsonify({
            'success': True,
            'valid': is_valid,
            'tool': tool_name
        }), 200
        
    except Exception as e:
        logger.error(f"Validate parameters error: {str(e)}")
        return jsonify({'error': 'Failed to validate parameters'}), 500


@tools_bp.route('/<tool_name>/command', methods=['POST'])
@require_auth()
def get_tool_command(tool_name):
    """Get the command that would be executed for a tool"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        target = data.get('target')
        parameters = data.get('parameters', {})
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Create tool instance
        tool = tool_registry.create_tool(tool_name)
        
        if not tool:
            return jsonify({'error': 'Tool not found'}), 404
        
        # Get command
        command = tool.get_command(target, parameters)
        
        return jsonify({
            'success': True,
            'command': command,
            'tool': tool_name,
            'target': target
        }), 200
        
    except Exception as e:
        logger.error(f"Get tool command error: {str(e)}")
        return jsonify({'error': 'Failed to get tool command'}), 500


@tools_bp.route('/registry/stats', methods=['GET'])
@require_auth()
def get_registry_stats():
    """Get tool registry statistics"""
    try:
        if not tool_registry._initialized:
            tool_registry.initialize()
        
        stats = tool_registry.get_registry_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        }), 200
        
    except Exception as e:
        logger.error(f"Get registry stats error: {str(e)}")
        return jsonify({'error': 'Failed to get registry stats'}), 500


@tools_bp.route('/nmap', methods=['POST'])
@require_auth()
def execute_nmap():
    """Execute nmap scan (legacy endpoint for backward compatibility)"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        target = data.get('target')
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Create nmap tool
        nmap_tool = tool_registry.create_tool('nmap')
        
        if not nmap_tool:
            return jsonify({'error': 'Nmap tool not available'}), 503
        
        # Execute nmap
        parameters = {
            'scan_type': data.get('scan_type', '-sS'),
            'ports': data.get('ports', '1-1000'),
            'timing': data.get('timing', '-T4'),
            'version_detection': data.get('version_detection', True),
            'script_scan': data.get('script_scan', True)
        }
        
        logger.info(f"Executing nmap against {target} by user {user.get('username')}")
        
        result = asyncio.run(nmap_tool.execute(target, parameters))
        
        return jsonify({
            'success': result.success,
            'scan_results': result.data,
            'raw_output': result.raw_output,
            'execution_time': result.execution_time,
            'command': result.command_executed
        }), 200 if result.success else 500
        
    except Exception as e:
        logger.error(f"Nmap execution error: {str(e)}")
        return jsonify({'error': 'Nmap execution failed'}), 500


@tools_bp.route('/nuclei', methods=['POST'])
@require_auth()
def execute_nuclei():
    """Execute nuclei scan (legacy endpoint for backward compatibility)"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        target = data.get('target')
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Create nuclei tool
        nuclei_tool = tool_registry.create_tool('nuclei')
        
        if not nuclei_tool:
            return jsonify({'error': 'Nuclei tool not available'}), 503
        
        # Execute nuclei
        parameters = {
            'severity': data.get('severity', 'critical,high,medium'),
            'tags': data.get('tags'),
            'concurrency': data.get('concurrency', 25),
            'output_format': data.get('output_format', 'json')
        }
        
        logger.info(f"Executing nuclei against {target} by user {user.get('username')}")
        
        result = asyncio.run(nuclei_tool.execute(target, parameters))
        
        return jsonify({
            'success': result.success,
            'vulnerabilities': result.data.get('vulnerabilities', []),
            'statistics': result.data.get('statistics', {}),
            'raw_output': result.raw_output,
            'execution_time': result.execution_time
        }), 200 if result.success else 500
        
    except Exception as e:
        logger.error(f"Nuclei execution error: {str(e)}")
        return jsonify({'error': 'Nuclei execution failed'}), 500