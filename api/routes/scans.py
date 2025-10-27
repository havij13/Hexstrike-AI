"""
Scan Routes

This module handles scan-related API endpoints.
"""

from flask import Blueprint, request, jsonify, current_app
from api.middleware.auth_middleware import require_auth, get_current_user
from core.decision_engine import IntelligentDecisionEngine
from agents.bugbounty_agent import BugBountyWorkflowManager
from agents.ctf_agent import CTFWorkflowManager
from tools.tool_registry import tool_registry
import asyncio
import logging
import uuid
from datetime import datetime

scans_bp = Blueprint('scans', __name__)
logger = logging.getLogger(__name__)

# Initialize components
decision_engine = IntelligentDecisionEngine()
bugbounty_agent = BugBountyWorkflowManager()
ctf_agent = CTFWorkflowManager()


@scans_bp.route('/', methods=['GET'])
@require_auth()
def list_scans():
    """List user's scans"""
    try:
        user = get_current_user()
        
        # In real implementation, fetch from database
        # Mock scan data
        scans = [
            {
                'id': 'scan_123',
                'target': 'example.com',
                'type': 'web_reconnaissance',
                'status': 'completed',
                'created_at': '2024-01-15T10:30:00Z',
                'completed_at': '2024-01-15T10:45:00Z',
                'vulnerabilities_found': 3
            },
            {
                'id': 'scan_456',
                'target': '192.168.1.1',
                'type': 'network_discovery',
                'status': 'running',
                'created_at': '2024-01-15T11:00:00Z',
                'progress': 65
            }
        ]
        
        return jsonify({
            'success': True,
            'scans': scans,
            'total': len(scans)
        }), 200
        
    except Exception as e:
        logger.error(f"List scans error: {str(e)}")
        return jsonify({'error': 'Failed to list scans'}), 500


@scans_bp.route('/', methods=['POST'])
@require_auth()
def create_scan():
    """Create a new scan"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        target = data.get('target')
        scan_type = data.get('type', 'reconnaissance')
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Generate scan ID
        scan_id = str(uuid.uuid4())
        
        # Analyze target
        profile = decision_engine.analyze_target(target)
        
        # Select appropriate tools
        tools = decision_engine.select_optimal_tools(profile, scan_type)
        
        # Create scan record
        scan_data = {
            'id': scan_id,
            'target': target,
            'type': scan_type,
            'status': 'created',
            'user_id': user.get('user_id'),
            'tenant_id': user.get('tenant_id'),
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'target_profile': profile.to_dict(),
            'selected_tools': tools,
            'parameters': data.get('parameters', {})
        }
        
        logger.info(f"Created scan {scan_id} for target {target} by user {user.get('username')}")
        
        return jsonify({
            'success': True,
            'scan': scan_data,
            'message': 'Scan created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f"Create scan error: {str(e)}")
        return jsonify({'error': 'Failed to create scan'}), 500


@scans_bp.route('/<scan_id>', methods=['GET'])
@require_auth()
def get_scan(scan_id):
    """Get scan details"""
    try:
        user = get_current_user()
        
        # In real implementation, fetch from database with user/tenant filtering
        # Mock scan data
        scan_data = {
            'id': scan_id,
            'target': 'example.com',
            'type': 'web_reconnaissance',
            'status': 'completed',
            'user_id': user.get('user_id'),
            'created_at': '2024-01-15T10:30:00Z',
            'completed_at': '2024-01-15T10:45:00Z',
            'results': {
                'vulnerabilities': [
                    {
                        'id': 'vuln_1',
                        'severity': 'high',
                        'title': 'SQL Injection',
                        'description': 'SQL injection vulnerability found in login form',
                        'url': 'https://example.com/login'
                    }
                ],
                'open_ports': [80, 443, 22],
                'technologies': ['Apache', 'PHP', 'MySQL']
            }
        }
        
        return jsonify({
            'success': True,
            'scan': scan_data
        }), 200
        
    except Exception as e:
        logger.error(f"Get scan error: {str(e)}")
        return jsonify({'error': 'Failed to get scan'}), 500


@scans_bp.route('/<scan_id>/start', methods=['POST'])
@require_auth()
def start_scan(scan_id):
    """Start a scan"""
    try:
        user = get_current_user()
        
        # In real implementation, update scan status and start execution
        logger.info(f"Starting scan {scan_id} by user {user.get('username')}")
        
        # Mock starting scan
        scan_data = {
            'id': scan_id,
            'status': 'running',
            'started_at': datetime.utcnow().isoformat() + 'Z',
            'progress': 0
        }
        
        return jsonify({
            'success': True,
            'scan': scan_data,
            'message': 'Scan started successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Start scan error: {str(e)}")
        return jsonify({'error': 'Failed to start scan'}), 500


@scans_bp.route('/<scan_id>/stop', methods=['POST'])
@require_auth()
def stop_scan(scan_id):
    """Stop a running scan"""
    try:
        user = get_current_user()
        
        # In real implementation, stop scan execution and update status
        logger.info(f"Stopping scan {scan_id} by user {user.get('username')}")
        
        scan_data = {
            'id': scan_id,
            'status': 'stopped',
            'stopped_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        return jsonify({
            'success': True,
            'scan': scan_data,
            'message': 'Scan stopped successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Stop scan error: {str(e)}")
        return jsonify({'error': 'Failed to stop scan'}), 500


@scans_bp.route('/<scan_id>/results', methods=['GET'])
@require_auth()
def get_scan_results(scan_id):
    """Get scan results"""
    try:
        user = get_current_user()
        
        # Mock scan results
        results = {
            'scan_id': scan_id,
            'status': 'completed',
            'summary': {
                'total_vulnerabilities': 5,
                'critical': 1,
                'high': 2,
                'medium': 1,
                'low': 1,
                'info': 0
            },
            'vulnerabilities': [
                {
                    'id': 'vuln_1',
                    'severity': 'critical',
                    'title': 'Remote Code Execution',
                    'description': 'RCE vulnerability in file upload functionality',
                    'cvss_score': 9.8,
                    'url': 'https://example.com/upload',
                    'evidence': 'Successful command execution: whoami'
                },
                {
                    'id': 'vuln_2',
                    'severity': 'high',
                    'title': 'SQL Injection',
                    'description': 'SQL injection in search parameter',
                    'cvss_score': 8.1,
                    'url': 'https://example.com/search?q=test',
                    'evidence': 'Database error revealed'
                }
            ],
            'scan_info': {
                'target': 'example.com',
                'tools_used': ['nmap', 'nuclei', 'gobuster'],
                'duration': 900,  # 15 minutes
                'requests_made': 1250
            }
        }
        
        return jsonify({
            'success': True,
            'results': results
        }), 200
        
    except Exception as e:
        logger.error(f"Get scan results error: {str(e)}")
        return jsonify({'error': 'Failed to get scan results'}), 500


@scans_bp.route('/<scan_id>', methods=['DELETE'])
@require_auth()
def delete_scan(scan_id):
    """Delete a scan"""
    try:
        user = get_current_user()
        
        # In real implementation, delete from database with proper authorization
        logger.info(f"Deleting scan {scan_id} by user {user.get('username')}")
        
        return jsonify({
            'success': True,
            'message': 'Scan deleted successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Delete scan error: {str(e)}")
        return jsonify({'error': 'Failed to delete scan'}), 500


@scans_bp.route('/workflows/bugbounty', methods=['POST'])
@require_auth()
def create_bugbounty_workflow():
    """Create bug bounty workflow"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        target = data.get('target')
        workflow_type = data.get('workflow_type', 'reconnaissance')
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Execute bug bounty agent
        result = asyncio.run(bugbounty_agent.execute(target, {
            'workflow_type': workflow_type,
            'priority_vulns': data.get('priority_vulns', ['rce', 'sqli', 'xss'])
        }))
        
        return jsonify({
            'success': result.success,
            'workflow': result.data,
            'message': result.message
        }), 200 if result.success else 500
        
    except Exception as e:
        logger.error(f"Bug bounty workflow error: {str(e)}")
        return jsonify({'error': 'Failed to create bug bounty workflow'}), 500


@scans_bp.route('/workflows/ctf', methods=['POST'])
@require_auth()
def create_ctf_workflow():
    """Create CTF workflow"""
    try:
        user = get_current_user()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        target = data.get('target')
        
        if not target:
            return jsonify({'error': 'Target is required'}), 400
        
        # Execute CTF agent
        result = asyncio.run(ctf_agent.execute(target, data))
        
        return jsonify({
            'success': result.success,
            'workflow': result.data,
            'message': result.message
        }), 200 if result.success else 500
        
    except Exception as e:
        logger.error(f"CTF workflow error: {str(e)}")
        return jsonify({'error': 'Failed to create CTF workflow'}), 500