"""
Enhanced Error Handler

This module provides intelligent error handling and recovery capabilities
for the HexStrike AI system.
"""

import logging
import traceback
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional, Callable, Union


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorType(Enum):
    """Enumeration of different error types for intelligent handling"""
    TIMEOUT = "timeout"
    PERMISSION_DENIED = "permission_denied"
    NETWORK_UNREACHABLE = "network_unreachable"
    RATE_LIMITED = "rate_limited"
    TOOL_NOT_FOUND = "tool_not_found"
    INVALID_PARAMETERS = "invalid_parameters"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    AUTHENTICATION_FAILED = "authentication_failed"
    TARGET_UNREACHABLE = "target_unreachable"
    PARSING_ERROR = "parsing_error"
    UNKNOWN = "unknown"


class RecoveryAction(Enum):
    """Types of recovery actions that can be taken"""
    RETRY_WITH_BACKOFF = "retry_with_backoff"
    RETRY_WITH_REDUCED_SCOPE = "retry_with_reduced_scope"
    SWITCH_TO_ALTERNATIVE_TOOL = "switch_to_alternative_tool"
    ADJUST_PARAMETERS = "adjust_parameters"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    ABORT_OPERATION = "abort_operation"


@dataclass
class ErrorContext:
    """Context information for error handling decisions"""
    tool_name: str
    target: str
    user_id: str
    tenant_id: str
    parameters: Dict[str, Any]
    error_type: str
    error_message: str
    stack_trace: str
    timestamp: str
    severity: ErrorSeverity
    attempt_count: int = 1
    system_resources: Dict[str, Any] = field(default_factory=dict)
    previous_errors: List['ErrorContext'] = field(default_factory=list)


@dataclass
class RecoveryStrategy:
    """Recovery strategy with configuration"""
    action: RecoveryAction
    parameters: Dict[str, Any]
    max_attempts: int = 3
    backoff_multiplier: float = 2.0
    timeout_seconds: int = 30


class EnhancedErrorHandler:
    """Enhanced error management system with intelligent recovery"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_patterns = self._load_error_patterns()
        self.recovery_strategies = self._load_recovery_strategies()
        self.error_history: List[ErrorContext] = []
        self.max_history_size = 1000

    def _load_error_patterns(self) -> Dict[str, ErrorType]:
        """Load error patterns for classification"""
        return {
            "timeout": ErrorType.TIMEOUT,
            "timed out": ErrorType.TIMEOUT,
            "connection timeout": ErrorType.TIMEOUT,
            "permission denied": ErrorType.PERMISSION_DENIED,
            "access denied": ErrorType.PERMISSION_DENIED,
            "forbidden": ErrorType.PERMISSION_DENIED,
            "network unreachable": ErrorType.NETWORK_UNREACHABLE,
            "no route to host": ErrorType.NETWORK_UNREACHABLE,
            "connection refused": ErrorType.NETWORK_UNREACHABLE,
            "rate limit": ErrorType.RATE_LIMITED,
            "too many requests": ErrorType.RATE_LIMITED,
            "command not found": ErrorType.TOOL_NOT_FOUND,
            "no such file": ErrorType.TOOL_NOT_FOUND,
            "invalid argument": ErrorType.INVALID_PARAMETERS,
            "invalid option": ErrorType.INVALID_PARAMETERS,
            "out of memory": ErrorType.RESOURCE_EXHAUSTED,
            "disk full": ErrorType.RESOURCE_EXHAUSTED,
            "authentication failed": ErrorType.AUTHENTICATION_FAILED,
            "login failed": ErrorType.AUTHENTICATION_FAILED,
            "unauthorized": ErrorType.AUTHENTICATION_FAILED,
            "host unreachable": ErrorType.TARGET_UNREACHABLE,
            "name resolution failed": ErrorType.TARGET_UNREACHABLE,
            "parse error": ErrorType.PARSING_ERROR,
            "syntax error": ErrorType.PARSING_ERROR,
            "invalid json": ErrorType.PARSING_ERROR
        }

    def _load_recovery_strategies(self) -> Dict[ErrorType, List[RecoveryStrategy]]:
        """Load recovery strategies for different error types"""
        return {
            ErrorType.TIMEOUT: [
                RecoveryStrategy(
                    action=RecoveryAction.RETRY_WITH_BACKOFF,
                    parameters={"initial_delay": 5, "max_delay": 60},
                    max_attempts=3
                ),
                RecoveryStrategy(
                    action=RecoveryAction.ADJUST_PARAMETERS,
                    parameters={"timeout_multiplier": 2.0},
                    max_attempts=2
                )
            ],
            ErrorType.RATE_LIMITED: [
                RecoveryStrategy(
                    action=RecoveryAction.RETRY_WITH_BACKOFF,
                    parameters={"initial_delay": 30, "max_delay": 300},
                    max_attempts=5,
                    backoff_multiplier=1.5
                ),
                RecoveryStrategy(
                    action=RecoveryAction.ADJUST_PARAMETERS,
                    parameters={"rate_limit_factor": 0.5},
                    max_attempts=2
                )
            ],
            ErrorType.PERMISSION_DENIED: [
                RecoveryStrategy(
                    action=RecoveryAction.ADJUST_PARAMETERS,
                    parameters={"use_sudo": True},
                    max_attempts=1
                ),
                RecoveryStrategy(
                    action=RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL,
                    parameters={},
                    max_attempts=1
                ),
                RecoveryStrategy(
                    action=RecoveryAction.ESCALATE_TO_HUMAN,
                    parameters={"reason": "Permission denied - manual intervention required"},
                    max_attempts=1
                )
            ],
            ErrorType.TOOL_NOT_FOUND: [
                RecoveryStrategy(
                    action=RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL,
                    parameters={},
                    max_attempts=1
                ),
                RecoveryStrategy(
                    action=RecoveryAction.ESCALATE_TO_HUMAN,
                    parameters={"reason": "Required tool not found - installation needed"},
                    max_attempts=1
                )
            ],
            ErrorType.NETWORK_UNREACHABLE: [
                RecoveryStrategy(
                    action=RecoveryAction.RETRY_WITH_BACKOFF,
                    parameters={"initial_delay": 10, "max_delay": 120},
                    max_attempts=3
                ),
                RecoveryStrategy(
                    action=RecoveryAction.ADJUST_PARAMETERS,
                    parameters={"use_proxy": True},
                    max_attempts=1
                )
            ],
            ErrorType.RESOURCE_EXHAUSTED: [
                RecoveryStrategy(
                    action=RecoveryAction.RETRY_WITH_REDUCED_SCOPE,
                    parameters={"scope_reduction_factor": 0.5},
                    max_attempts=2
                ),
                RecoveryStrategy(
                    action=RecoveryAction.GRACEFUL_DEGRADATION,
                    parameters={"fallback_mode": True},
                    max_attempts=1
                )
            ],
            ErrorType.INVALID_PARAMETERS: [
                RecoveryStrategy(
                    action=RecoveryAction.ADJUST_PARAMETERS,
                    parameters={"use_defaults": True},
                    max_attempts=1
                ),
                RecoveryStrategy(
                    action=RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL,
                    parameters={},
                    max_attempts=1
                )
            ],
            ErrorType.TARGET_UNREACHABLE: [
                RecoveryStrategy(
                    action=RecoveryAction.RETRY_WITH_BACKOFF,
                    parameters={"initial_delay": 15, "max_delay": 180},
                    max_attempts=2
                ),
                RecoveryStrategy(
                    action=RecoveryAction.GRACEFUL_DEGRADATION,
                    parameters={"skip_target": True},
                    max_attempts=1
                )
            ],
            ErrorType.PARSING_ERROR: [
                RecoveryStrategy(
                    action=RecoveryAction.ADJUST_PARAMETERS,
                    parameters={"output_format": "json"},
                    max_attempts=1
                ),
                RecoveryStrategy(
                    action=RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL,
                    parameters={},
                    max_attempts=1
                )
            ]
        }

    def classify_error(self, error_message: str, exception: Exception = None) -> ErrorType:
        """Classify error based on message and exception type"""
        error_message_lower = error_message.lower()

        # Check for specific patterns
        for pattern, error_type in self.error_patterns.items():
            if pattern in error_message_lower:
                return error_type

        # Check exception type
        if exception:
            if isinstance(exception, TimeoutError):
                return ErrorType.TIMEOUT
            elif isinstance(exception, PermissionError):
                return ErrorType.PERMISSION_DENIED
            elif isinstance(exception, FileNotFoundError):
                return ErrorType.TOOL_NOT_FOUND
            elif isinstance(exception, ConnectionError):
                return ErrorType.NETWORK_UNREACHABLE
            elif isinstance(exception, ValueError):
                return ErrorType.INVALID_PARAMETERS

        return ErrorType.UNKNOWN

    def determine_severity(self, error_type: ErrorType, context: Dict[str, Any]) -> ErrorSeverity:
        """Determine error severity based on type and context"""
        # Critical errors that stop execution
        if error_type in [ErrorType.RESOURCE_EXHAUSTED, ErrorType.AUTHENTICATION_FAILED]:
            return ErrorSeverity.CRITICAL

        # High severity errors that significantly impact functionality
        if error_type in [ErrorType.TOOL_NOT_FOUND, ErrorType.PERMISSION_DENIED]:
            return ErrorSeverity.HIGH

        # Medium severity errors that can often be recovered from
        if error_type in [ErrorType.TIMEOUT, ErrorType.RATE_LIMITED, ErrorType.NETWORK_UNREACHABLE]:
            return ErrorSeverity.MEDIUM

        # Low severity errors that are minor issues
        return ErrorSeverity.LOW

    async def handle_error(self, error_context: ErrorContext) -> Dict[str, Any]:
        """Handle error with intelligent recovery"""
        # Log the error
        self._log_error(error_context)

        # Add to history
        self._add_to_history(error_context)

        # Determine recovery strategy
        recovery_action = self._determine_recovery_action(error_context)

        if recovery_action:
            try:
                # Execute recovery
                result = await self._execute_recovery(error_context, recovery_action)
                return result
            except Exception as e:
                self.logger.error(f"Recovery action failed: {str(e)}")
                return {"status": "failed", "error": error_context.error_message, "recovery_failed": True}

        return {"status": "failed", "error": error_context.error_message}

    def _log_error(self, error_context: ErrorContext):
        """Log error with structured information"""
        log_data = {
            "tool": error_context.tool_name,
            "target": error_context.target,
            "user_id": error_context.user_id,
            "tenant_id": error_context.tenant_id,
            "error_type": error_context.error_type,
            "severity": error_context.severity.value,
            "attempt": error_context.attempt_count,
            "timestamp": error_context.timestamp
        }

        if error_context.severity == ErrorSeverity.CRITICAL:
            self.logger.critical(f"Critical error in {error_context.tool_name}: {error_context.error_message}", extra=log_data)
        elif error_context.severity == ErrorSeverity.HIGH:
            self.logger.error(f"High severity error in {error_context.tool_name}: {error_context.error_message}", extra=log_data)
        elif error_context.severity == ErrorSeverity.MEDIUM:
            self.logger.warning(f"Medium severity error in {error_context.tool_name}: {error_context.error_message}", extra=log_data)
        else:
            self.logger.info(f"Low severity error in {error_context.tool_name}: {error_context.error_message}", extra=log_data)

    def _add_to_history(self, error_context: ErrorContext):
        """Add error to history for pattern analysis"""
        self.error_history.append(error_context)

        # Maintain history size limit
        if len(self.error_history) > self.max_history_size:
            self.error_history = self.error_history[-self.max_history_size:]

    def _determine_recovery_action(self, error_context: ErrorContext) -> Optional[RecoveryStrategy]:
        """Determine the best recovery action for the error"""
        error_type = ErrorType(error_context.error_type) if isinstance(error_context.error_type, str) else error_context.error_type

        strategies = self.recovery_strategies.get(error_type, [])

        if not strategies:
            return None

        # Select strategy based on attempt count and previous failures
        for strategy in strategies:
            if error_context.attempt_count <= strategy.max_attempts:
                return strategy

        return None

    async def _execute_recovery(self, error_context: ErrorContext, strategy: RecoveryStrategy) -> Dict[str, Any]:
        """Execute the recovery strategy"""
        action = strategy.action

        if action == RecoveryAction.RETRY_WITH_BACKOFF:
            return await self._retry_with_backoff(error_context, strategy)
        elif action == RecoveryAction.RETRY_WITH_REDUCED_SCOPE:
            return await self._retry_with_reduced_scope(error_context, strategy)
        elif action == RecoveryAction.SWITCH_TO_ALTERNATIVE_TOOL:
            return await self._switch_to_alternative_tool(error_context, strategy)
        elif action == RecoveryAction.ADJUST_PARAMETERS:
            return await self._adjust_parameters(error_context, strategy)
        elif action == RecoveryAction.ESCALATE_TO_HUMAN:
            return await self._escalate_to_human(error_context, strategy)
        elif action == RecoveryAction.GRACEFUL_DEGRADATION:
            return await self._graceful_degradation(error_context, strategy)
        elif action == RecoveryAction.ABORT_OPERATION:
            return await self._abort_operation(error_context, strategy)

        return {"status": "failed", "error": "Unknown recovery action"}

    async def _retry_with_backoff(self, error_context: ErrorContext, strategy: RecoveryStrategy) -> Dict[str, Any]:
        """Implement retry with exponential backoff"""
        import asyncio

        initial_delay = strategy.parameters.get("initial_delay", 5)
        max_delay = strategy.parameters.get("max_delay", 60)

        delay = min(initial_delay * (strategy.backoff_multiplier ** (error_context.attempt_count - 1)), max_delay)

        self.logger.info(f"Retrying {error_context.tool_name} after {delay} seconds (attempt {error_context.attempt_count})")

        await asyncio.sleep(delay)

        return {
            "status": "retry_scheduled",
            "action": "retry_with_backoff",
            "delay": delay,
            "attempt": error_context.attempt_count + 1
        }

    async def _retry_with_reduced_scope(self, error_context: ErrorContext, strategy: RecoveryStrategy) -> Dict[str, Any]:
        """Retry with reduced scope/parameters"""
        reduction_factor = strategy.parameters.get("scope_reduction_factor", 0.5)

        # Adjust parameters to reduce scope
        adjusted_params = error_context.parameters.copy()

        # Reduce common parameters that might cause resource issues
        if "threads" in adjusted_params:
            adjusted_params["threads"] = max(1, int(adjusted_params["threads"] * reduction_factor))
        if "timeout" in adjusted_params:
            adjusted_params["timeout"] = int(adjusted_params["timeout"] * reduction_factor)
        if "rate" in adjusted_params:
            adjusted_params["rate"] = int(adjusted_params["rate"] * reduction_factor)

        return {
            "status": "retry_scheduled",
            "action": "retry_with_reduced_scope",
            "adjusted_parameters": adjusted_params,
            "attempt": error_context.attempt_count + 1
        }

    async def _switch_to_alternative_tool(self, error_context: ErrorContext, strategy: RecoveryStrategy) -> Dict[str, Any]:
        """Switch to an alternative tool"""
        # Tool alternatives mapping
        alternatives = {
            "nmap": ["rustscan", "masscan"],
            "gobuster": ["dirsearch", "feroxbuster", "ffuf"],
            "nuclei": ["jaeles", "nikto"],
            "sqlmap": ["sqlmap", "ghauri"],
            "amass": ["subfinder", "assetfinder"],
            "ghidra": ["radare2", "ida"],
            "burpsuite": ["owasp-zap", "caido"]
        }

        tool_alternatives = alternatives.get(error_context.tool_name, [])

        if tool_alternatives:
            alternative_tool = tool_alternatives[0]  # Use first alternative
            return {
                "status": "tool_switched",
                "action": "switch_to_alternative_tool",
                "original_tool": error_context.tool_name,
                "alternative_tool": alternative_tool,
                "parameters": error_context.parameters
            }

        return {"status": "failed", "error": "No alternative tool available"}

    async def _adjust_parameters(self, error_context: ErrorContext, strategy: RecoveryStrategy) -> Dict[str, Any]:
        """Adjust parameters to fix the issue"""
        adjusted_params = error_context.parameters.copy()

        # Apply parameter adjustments based on strategy
        for key, value in strategy.parameters.items():
            if key == "timeout_multiplier":
                if "timeout" in adjusted_params:
                    adjusted_params["timeout"] = int(adjusted_params["timeout"] * value)
            elif key == "rate_limit_factor":
                if "rate" in adjusted_params:
                    adjusted_params["rate"] = int(adjusted_params["rate"] * value)
                if "threads" in adjusted_params:
                    adjusted_params["threads"] = max(1, int(adjusted_params["threads"] * value))
            elif key == "use_sudo":
                adjusted_params["use_sudo"] = value
            elif key == "use_proxy":
                adjusted_params["use_proxy"] = value
            elif key == "use_defaults":
                # Reset to default parameters
                adjusted_params = {"target": error_context.target}
            elif key == "output_format":
                adjusted_params["output_format"] = value

        return {
            "status": "parameters_adjusted",
            "action": "adjust_parameters",
            "adjusted_parameters": adjusted_params,
            "attempt": error_context.attempt_count + 1
        }

    async def _escalate_to_human(self, error_context: ErrorContext, strategy: RecoveryStrategy) -> Dict[str, Any]:
        """Escalate to human intervention"""
        reason = strategy.parameters.get("reason", "Automatic recovery failed")

        # In a real implementation, this would create a ticket or notification
        self.logger.warning(f"Escalating to human: {reason} - Tool: {error_context.tool_name}, Target: {error_context.target}")

        return {
            "status": "escalated",
            "action": "escalate_to_human",
            "reason": reason,
            "tool": error_context.tool_name,
            "target": error_context.target,
            "error": error_context.error_message
        }

    async def _graceful_degradation(self, error_context: ErrorContext, strategy: RecoveryStrategy) -> Dict[str, Any]:
        """Implement graceful degradation"""
        fallback_mode = strategy.parameters.get("fallback_mode", False)
        skip_target = strategy.parameters.get("skip_target", False)

        if skip_target:
            return {
                "status": "target_skipped",
                "action": "graceful_degradation",
                "reason": "Target unreachable - continuing with other targets"
            }

        if fallback_mode:
            return {
                "status": "fallback_mode",
                "action": "graceful_degradation",
                "reason": "Using reduced functionality due to resource constraints"
            }

        return {
            "status": "degraded",
            "action": "graceful_degradation",
            "reason": "Operating in degraded mode"
        }

    async def _abort_operation(self, error_context: ErrorContext, strategy: RecoveryStrategy) -> Dict[str, Any]:
        """Abort the operation"""
        reason = strategy.parameters.get("reason", "Unrecoverable error")

        return {
            "status": "aborted",
            "action": "abort_operation",
            "reason": reason,
            "error": error_context.error_message
        }

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics from history"""
        if not self.error_history:
            return {"total_errors": 0}

        total_errors = len(self.error_history)
        error_types = {}
        severity_counts = {}
        tool_errors = {}

        for error in self.error_history:
            # Count by error type
            error_type = error.error_type
            error_types[error_type] = error_types.get(error_type, 0) + 1

            # Count by severity
            severity = error.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

            # Count by tool
            tool = error.tool_name
            tool_errors[tool] = tool_errors.get(tool, 0) + 1

        return {
            "total_errors": total_errors,
            "error_types": error_types,
            "severity_distribution": severity_counts,
            "tool_error_counts": tool_errors,
            "most_common_error": max(error_types.items(), key=lambda x: x[1])[0] if error_types else None,
            "most_problematic_tool": max(tool_errors.items(), key=lambda x: x[1])[0] if tool_errors else None
        }