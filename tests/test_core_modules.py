"""
Tests for Core Modules

This module contains unit tests for the core application modules.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from flask import Flask
from core.app import create_app, register_blueprints, register_error_handlers, initialize_extensions
from core.visual_engine import ModernVisualEngine
from core.error_handler import (
    EnhancedErrorHandler, 
    ErrorContext, 
    ErrorSeverity, 
    ErrorType, 
    RecoveryAction,
    RecoveryStrategy
)
from datetime import datetime


class TestFlaskAppFactory:
    """Test cases for Flask application factory"""

    def test_create_app_default(self):
        """Test creating app with default configuration"""
        app = create_app(testing=True)
        
        assert isinstance(app, Flask)
        assert app.config['TESTING'] is True
        assert app.config['JSON_SORT_KEYS'] is False

    def test_create_app_with_config(self):
        """Test creating app with specific configuration"""
        app = create_app('production', testing=False)
        
        assert isinstance(app, Flask)
        assert app.config.get('TESTING') is not True

    def test_register_blueprints(self):
        """Test blueprint registration"""
        app = create_app(testing=True)
        
        # Check that blueprints are registered
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        
        assert 'auth' in blueprint_names
        assert 'scans' in blueprint_names
        assert 'tools' in blueprint_names
        assert 'admin' in blueprint_names
        assert 'webhooks' in blueprint_names

    def test_error_handlers_registration(self):
        """Test error handlers are registered"""
        app = create_app(testing=True)
        
        with app.test_client() as client:
            # Test 404 handler
            response = client.get('/nonexistent-endpoint')
            assert response.status_code == 404
            assert 'error' in response.get_json()

    def test_app_context(self):
        """Test app context functionality"""
        from flask import current_app
        app = create_app(testing=True)
        
        with app.app_context():
            assert app == current_app


class TestModernVisualEngine:
    """Test cases for ModernVisualEngine"""

    def test_create_banner(self):
        """Test banner creation"""
        banner = ModernVisualEngine.create_banner("localhost", 8080)
        
        assert isinstance(banner, str)
        assert "HexStrike" in banner
        assert "localhost:8080" in banner
        assert "Blood-Red Offensive Intelligence Core" in banner

    def test_create_progress_bar(self):
        """Test progress bar creation"""
        progress_bar = ModernVisualEngine.create_progress_bar(50, 100, 40, "nmap")
        
        assert isinstance(progress_bar, str)
        assert "nmap" in progress_bar
        assert "50.0%" in progress_bar
        assert "█" in progress_bar or "░" in progress_bar

    def test_render_progress_bar_cyber_style(self):
        """Test progress bar rendering with cyber style"""
        progress_bar = ModernVisualEngine.render_progress_bar(
            0.75, width=20, style='cyber', label="Scanning"
        )
        
        assert isinstance(progress_bar, str)
        assert "Scanning" in progress_bar
        assert "75.0%" in progress_bar

    def test_render_progress_bar_with_eta(self):
        """Test progress bar with ETA and speed"""
        progress_bar = ModernVisualEngine.render_progress_bar(
            0.5, width=30, eta=120.5, speed="10 req/s"
        )
        
        assert isinstance(progress_bar, str)
        assert "50.0%" in progress_bar
        assert "ETA: 120.5s" in progress_bar
        assert "Speed: 10 req/s" in progress_bar

    def test_create_live_dashboard_empty(self):
        """Test live dashboard with no processes"""
        dashboard = ModernVisualEngine.create_live_dashboard({})
        
        assert isinstance(dashboard, str)
        assert "HEXSTRIKE LIVE DASHBOARD" in dashboard
        assert "No active processes" in dashboard

    def test_create_live_dashboard_with_processes(self):
        """Test live dashboard with active processes"""
        processes = {
            123: {
                'status': 'running',
                'command': 'nmap -sS example.com',
                'duration': 45
            },
            456: {
                'status': 'completed',
                'command': 'nuclei -u https://example.com',
                'duration': 120
            }
        }
        
        dashboard = ModernVisualEngine.create_live_dashboard(processes)
        
        assert isinstance(dashboard, str)
        assert "HEXSTRIKE LIVE DASHBOARD" in dashboard
        assert "PID 123" in dashboard
        assert "PID 456" in dashboard
        assert "nmap" in dashboard
        assert "nuclei" in dashboard

    def test_format_vulnerability_card(self):
        """Test vulnerability card formatting"""
        vuln_data = {
            'severity': 'high',
            'name': 'SQL Injection',
            'description': 'SQL injection vulnerability in login form'
        }
        
        card = ModernVisualEngine.format_vulnerability_card(vuln_data)
        
        assert isinstance(card, str)
        assert "VULNERABILITY DETECTED" in card
        assert "SQL Injection" in card
        assert "HIGH" in card
        assert "SQL injection vulnerability" in card

    def test_format_error_card(self):
        """Test error card formatting"""
        card = ModernVisualEngine.format_error_card(
            "TIMEOUT", "nmap", "Connection timed out", "Retry with increased timeout"
        )
        
        assert isinstance(card, str)
        assert "ERROR DETECTED" in card
        assert "nmap" in card
        assert "TIMEOUT" in card
        assert "Connection timed out" in card
        assert "Retry with increased timeout" in card

    def test_format_tool_status(self):
        """Test tool status formatting"""
        status = ModernVisualEngine.format_tool_status("nmap", "RUNNING", "example.com", 0.65)
        
        assert isinstance(status, str)
        assert "NMAP" in status
        assert "RUNNING" in status
        assert "example.com" in status
        assert "65.0%" in status

    def test_format_highlighted_text(self):
        """Test text highlighting"""
        highlighted = ModernVisualEngine.format_highlighted_text("CRITICAL ERROR", "RED")
        
        assert isinstance(highlighted, str)
        assert "CRITICAL ERROR" in highlighted

    def test_format_vulnerability_severity(self):
        """Test vulnerability severity formatting"""
        severity = ModernVisualEngine.format_vulnerability_severity("CRITICAL", 5)
        
        assert isinstance(severity, str)
        assert "CRITICAL" in severity
        assert "(5)" in severity

    def test_create_section_header(self):
        """Test section header creation"""
        header = ModernVisualEngine.create_section_header("SCAN RESULTS", "🎯", "FIRE_RED")
        
        assert isinstance(header, str)
        assert "SCAN RESULTS" in header
        assert "🎯" in header
        assert "═" in header

    def test_format_command_execution(self):
        """Test command execution formatting"""
        formatted = ModernVisualEngine.format_command_execution(
            "nmap -sS example.com", "SUCCESS", 45.2
        )
        
        assert isinstance(formatted, str)
        assert "nmap -sS example.com" in formatted
        assert "SUCCESS" in formatted
        assert "(45.20s)" in formatted

    def test_format_scan_results_empty(self):
        """Test scan results formatting with empty results"""
        formatted = ModernVisualEngine.format_scan_results({})
        
        assert isinstance(formatted, str)
        assert "No results to display" in formatted

    def test_format_scan_results_with_data(self):
        """Test scan results formatting with data"""
        results = {
            'summary': {
                'target': 'example.com',
                'duration': '15 minutes',
                'status': 'completed'
            },
            'vulnerabilities': [
                {
                    'severity': 'high',
                    'name': 'SQL Injection',
                    'description': 'SQL injection in login form'
                }
            ]
        }
        
        formatted = ModernVisualEngine.format_scan_results(results)
        
        assert isinstance(formatted, str)
        assert "SCAN RESULTS" in formatted
        assert "example.com" in formatted
        assert "15 minutes" in formatted
        assert "completed" in formatted
        assert "SQL Injection" in formatted


class TestEnhancedErrorHandler:
    """Test cases for EnhancedErrorHandler"""

    def setup_method(self):
        """Setup test fixtures"""
        self.error_handler = EnhancedErrorHandler()

    def test_initialization(self):
        """Test error handler initialization"""
        assert isinstance(self.error_handler.error_patterns, dict)
        assert isinstance(self.error_handler.recovery_strategies, dict)
        assert isinstance(self.error_handler.error_history, list)
        assert len(self.error_handler.error_history) == 0

    def test_classify_error_timeout(self):
        """Test error classification for timeout"""
        error_type = self.error_handler.classify_error("Connection timeout occurred")
        assert error_type == ErrorType.TIMEOUT

    def test_classify_error_permission_denied(self):
        """Test error classification for permission denied"""
        error_type = self.error_handler.classify_error("Permission denied")
        assert error_type == ErrorType.PERMISSION_DENIED

    def test_classify_error_with_exception(self):
        """Test error classification with exception"""
        error_type = self.error_handler.classify_error(
            "Some error", TimeoutError("Timeout")
        )
        assert error_type == ErrorType.TIMEOUT

    def test_classify_error_unknown(self):
        """Test error classification for unknown error"""
        error_type = self.error_handler.classify_error("Some unknown error")
        assert error_type == ErrorType.UNKNOWN

    def test_determine_severity_critical(self):
        """Test severity determination for critical errors"""
        severity = self.error_handler.determine_severity(
            ErrorType.RESOURCE_EXHAUSTED, {}
        )
        assert severity == ErrorSeverity.CRITICAL

    def test_determine_severity_high(self):
        """Test severity determination for high severity errors"""
        severity = self.error_handler.determine_severity(
            ErrorType.TOOL_NOT_FOUND, {}
        )
        assert severity == ErrorSeverity.HIGH

    def test_determine_severity_medium(self):
        """Test severity determination for medium severity errors"""
        severity = self.error_handler.determine_severity(
            ErrorType.TIMEOUT, {}
        )
        assert severity == ErrorSeverity.MEDIUM

    def test_determine_severity_low(self):
        """Test severity determination for low severity errors"""
        severity = self.error_handler.determine_severity(
            ErrorType.PARSING_ERROR, {}
        )
        assert severity == ErrorSeverity.LOW

    @pytest.mark.asyncio
    async def test_handle_error_with_recovery(self):
        """Test error handling with recovery"""
        error_context = ErrorContext(
            tool_name="nmap",
            target="example.com",
            user_id="user_123",
            tenant_id="tenant_123",
            parameters={"timeout": 30},
            error_type=ErrorType.TIMEOUT.value,
            error_message="Connection timeout",
            stack_trace="",
            timestamp=datetime.utcnow().isoformat(),
            severity=ErrorSeverity.MEDIUM
        )
        
        result = await self.error_handler.handle_error(error_context)
        
        assert isinstance(result, dict)
        assert "status" in result

    def test_determine_recovery_action_timeout(self):
        """Test recovery action determination for timeout"""
        error_context = ErrorContext(
            tool_name="nmap",
            target="example.com",
            user_id="user_123",
            tenant_id="tenant_123",
            parameters={},
            error_type=ErrorType.TIMEOUT.value,
            error_message="Timeout",
            stack_trace="",
            timestamp=datetime.utcnow().isoformat(),
            severity=ErrorSeverity.MEDIUM,
            attempt_count=1
        )
        
        strategy = self.error_handler._determine_recovery_action(error_context)
        
        assert strategy is not None
        assert isinstance(strategy, RecoveryStrategy)
        assert strategy.action in [RecoveryAction.RETRY_WITH_BACKOFF, RecoveryAction.ADJUST_PARAMETERS]

    def test_determine_recovery_action_max_attempts(self):
        """Test recovery action when max attempts exceeded"""
        error_context = ErrorContext(
            tool_name="nmap",
            target="example.com",
            user_id="user_123",
            tenant_id="tenant_123",
            parameters={},
            error_type=ErrorType.TIMEOUT.value,
            error_message="Timeout",
            stack_trace="",
            timestamp=datetime.utcnow().isoformat(),
            severity=ErrorSeverity.MEDIUM,
            attempt_count=10  # Exceeds max attempts
        )
        
        strategy = self.error_handler._determine_recovery_action(error_context)
        
        assert strategy is None

    @pytest.mark.asyncio
    async def test_retry_with_backoff(self):
        """Test retry with backoff recovery"""
        error_context = ErrorContext(
            tool_name="nmap",
            target="example.com",
            user_id="user_123",
            tenant_id="tenant_123",
            parameters={},
            error_type=ErrorType.TIMEOUT.value,
            error_message="Timeout",
            stack_trace="",
            timestamp=datetime.utcnow().isoformat(),
            severity=ErrorSeverity.MEDIUM,
            attempt_count=1
        )
        
        strategy = RecoveryStrategy(
            action=RecoveryAction.RETRY_WITH_BACKOFF,
            parameters={"initial_delay": 1, "max_delay": 5}
        )
        
        result = await self.error_handler._retry_with_backoff(error_context, strategy)
        
        assert result["status"] == "retry_scheduled"
        assert result["action"] == "retry_with_backoff"
        assert "delay" in result
        assert result["attempt"] == 2

    @pytest.mark.asyncio
    async def test_switch_to_alternative_tool(self):
        """Test switching to alternative tool"""
        error_context = ErrorContext(
            tool_name="nmap",
            target="example.com",
            user_id="user_123",
            tenant_id="tenant_123",
            parameters={},
            error_type=ErrorType.TOOL_NOT_FOUND.value,
            error_message="Tool not found",
            stack_trace="",
            timestamp=datetime.utcnow().isoformat(),
            severity=ErrorSeverity.HIGH
        )
        
        strategy = RecoveryStrategy(
            action=RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL,
            parameters={}
        )
        
        result = await self.error_handler._switch_to_alternative_tool(error_context, strategy)
        
        assert result["status"] == "tool_switched"
        assert result["original_tool"] == "nmap"
        assert result["alternative_tool"] in ["rustscan", "masscan"]

    @pytest.mark.asyncio
    async def test_adjust_parameters(self):
        """Test parameter adjustment recovery"""
        error_context = ErrorContext(
            tool_name="nmap",
            target="example.com",
            user_id="user_123",
            tenant_id="tenant_123",
            parameters={"timeout": 30, "threads": 10},
            error_type=ErrorType.TIMEOUT.value,
            error_message="Timeout",
            stack_trace="",
            timestamp=datetime.utcnow().isoformat(),
            severity=ErrorSeverity.MEDIUM
        )
        
        strategy = RecoveryStrategy(
            action=RecoveryAction.ADJUST_PARAMETERS,
            parameters={"timeout_multiplier": 2.0}
        )
        
        result = await self.error_handler._adjust_parameters(error_context, strategy)
        
        assert result["status"] == "parameters_adjusted"
        assert result["adjusted_parameters"]["timeout"] == 60  # 30 * 2.0

    def test_get_error_statistics_empty(self):
        """Test error statistics with empty history"""
        stats = self.error_handler.get_error_statistics()
        
        assert stats["total_errors"] == 0

    def test_get_error_statistics_with_data(self):
        """Test error statistics with error history"""
        # Add some test errors
        error1 = ErrorContext(
            tool_name="nmap",
            target="example.com",
            user_id="user_123",
            tenant_id="tenant_123",
            parameters={},
            error_type=ErrorType.TIMEOUT.value,
            error_message="Timeout",
            stack_trace="",
            timestamp=datetime.utcnow().isoformat(),
            severity=ErrorSeverity.MEDIUM
        )
        
        error2 = ErrorContext(
            tool_name="nuclei",
            target="example.com",
            user_id="user_123",
            tenant_id="tenant_123",
            parameters={},
            error_type=ErrorType.RATE_LIMITED.value,
            error_message="Rate limited",
            stack_trace="",
            timestamp=datetime.utcnow().isoformat(),
            severity=ErrorSeverity.LOW
        )
        
        self.error_handler._add_to_history(error1)
        self.error_handler._add_to_history(error2)
        
        stats = self.error_handler.get_error_statistics()
        
        assert stats["total_errors"] == 2
        assert ErrorType.TIMEOUT.value in stats["error_types"]
        assert ErrorType.RATE_LIMITED.value in stats["error_types"]
        assert "medium" in stats["severity_distribution"]
        assert "low" in stats["severity_distribution"]
        assert "nmap" in stats["tool_error_counts"]
        assert "nuclei" in stats["tool_error_counts"]