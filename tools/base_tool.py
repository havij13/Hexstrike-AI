"""
Base Tool Interface

This module provides the abstract base class for all security tools in the HexStrike system.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List, Optional
import logging
import time


class ToolStatus(Enum):
    """Tool execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class ToolResult:
    """Standard result format for tool operations"""
    success: bool
    data: Dict[str, Any]
    raw_output: str
    error_message: str = ""
    status: ToolStatus = ToolStatus.COMPLETED
    execution_time: float = 0.0
    command_executed: str = ""
    exit_code: int = 0


class BaseTool(ABC):
    """Abstract base class for all security tools"""

    def __init__(self, name: str, category: str, config: Dict[str, Any] = None):
        self.name = name
        self.category = category
        self.config = config or {}
        self.status = ToolStatus.IDLE
        self.logger = logging.getLogger(f"tools.{category}.{name}")
        self.execution_history: List[ToolResult] = []
        self.max_history_size = 50

    @abstractmethod
    async def execute(self, target: str, parameters: Dict[str, Any] = None) -> ToolResult:
        """
        Execute the tool against a target
        
        Args:
            target: The target to scan/test
            parameters: Tool-specific parameters
            
        Returns:
            ToolResult: Result of the tool execution
        """
        pass

    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate tool parameters
        
        Args:
            parameters: Parameters to validate
            
        Returns:
            bool: True if parameters are valid
        """
        pass

    @abstractmethod
    def get_command(self, target: str, parameters: Dict[str, Any] = None) -> str:
        """
        Get the command that would be executed
        
        Args:
            target: The target
            parameters: Tool parameters
            
        Returns:
            str: Command string
        """
        pass

    def get_capabilities(self) -> List[str]:
        """
        Get list of tool capabilities
        
        Returns:
            List[str]: List of capabilities
        """
        return []

    def get_supported_targets(self) -> List[str]:
        """
        Get list of supported target types
        
        Returns:
            List[str]: List of target types (url, ip, domain, file, etc.)
        """
        return ["url", "ip", "domain"]

    def get_status(self) -> ToolStatus:
        """Get current tool status"""
        return self.status

    def set_status(self, status: ToolStatus):
        """Set tool status"""
        self.status = status
        self.logger.debug(f"Tool {self.name} status changed to {status.value}")

    def add_result(self, result: ToolResult):
        """Add result to execution history"""
        self.execution_history.append(result)
        
        # Maintain history size limit
        if len(self.execution_history) > self.max_history_size:
            self.execution_history = self.execution_history[-self.max_history_size:]

    def get_execution_history(self) -> List[ToolResult]:
        """Get execution history"""
        return self.execution_history.copy()

    def get_last_result(self) -> Optional[ToolResult]:
        """Get the last execution result"""
        return self.execution_history[-1] if self.execution_history else None

    def reset(self):
        """Reset tool to initial state"""
        self.status = ToolStatus.IDLE
        self.execution_history.clear()
        self.logger.info(f"Tool {self.name} reset to initial state")

    def configure(self, config: Dict[str, Any]):
        """Update tool configuration"""
        self.config.update(config)
        self.logger.info(f"Tool {self.name} configuration updated")

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config.copy()

    def get_statistics(self) -> Dict[str, Any]:
        """Get tool execution statistics"""
        if not self.execution_history:
            return {
                "total_executions": 0,
                "success_rate": 0.0,
                "average_execution_time": 0.0,
                "total_targets_scanned": 0
            }

        total_executions = len(self.execution_history)
        successful_executions = sum(1 for result in self.execution_history if result.success)
        success_rate = successful_executions / total_executions
        
        total_time = sum(result.execution_time for result in self.execution_history)
        average_execution_time = total_time / total_executions

        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": total_executions - successful_executions,
            "success_rate": success_rate,
            "average_execution_time": average_execution_time,
            "total_targets_scanned": total_executions,  # Simplified
            "current_status": self.status.value
        }

    def get_default_parameters(self) -> Dict[str, Any]:
        """Get default parameters for the tool"""
        return {}

    def get_parameter_schema(self) -> Dict[str, Any]:
        """Get parameter schema for validation"""
        return {
            "type": "object",
            "properties": {},
            "required": []
        }

    def is_available(self) -> bool:
        """Check if tool is available on the system"""
        # This would typically check if the tool binary exists
        # For now, return True as a placeholder
        return True

    def get_version(self) -> str:
        """Get tool version"""
        return "unknown"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, category={self.category}, status={self.status.value})"

    def __repr__(self) -> str:
        return self.__str__()