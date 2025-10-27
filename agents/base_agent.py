"""
Base Agent Class

This module provides the abstract base class for all AI agents in the HexStrike system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging


class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class AgentResult:
    """Standard result format for agent operations"""
    success: bool
    data: Dict[str, Any]
    message: str
    status: AgentStatus
    execution_time: float = 0.0
    errors: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class BaseAgent(ABC):
    """Abstract base class for all AI agents"""

    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}
        self.status = AgentStatus.IDLE
        self.logger = logging.getLogger(f"agents.{name}")
        self.execution_history: List[AgentResult] = []
        self.max_history_size = 100

    @abstractmethod
    async def execute(self, target: str, parameters: Dict[str, Any] = None) -> AgentResult:
        """
        Execute the agent's main functionality
        
        Args:
            target: The target to operate on
            parameters: Additional parameters for execution
            
        Returns:
            AgentResult: Result of the execution
        """
        pass

    @abstractmethod
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate input parameters
        
        Args:
            parameters: Parameters to validate
            
        Returns:
            bool: True if parameters are valid
        """
        pass

    def get_capabilities(self) -> List[str]:
        """
        Get list of agent capabilities
        
        Returns:
            List[str]: List of capabilities
        """
        return []

    def get_status(self) -> AgentStatus:
        """Get current agent status"""
        return self.status

    def set_status(self, status: AgentStatus):
        """Set agent status"""
        self.status = status
        self.logger.info(f"Agent {self.name} status changed to {status.value}")

    def add_result(self, result: AgentResult):
        """Add result to execution history"""
        self.execution_history.append(result)
        
        # Maintain history size limit
        if len(self.execution_history) > self.max_history_size:
            self.execution_history = self.execution_history[-self.max_history_size:]

    def get_execution_history(self) -> List[AgentResult]:
        """Get execution history"""
        return self.execution_history.copy()

    def get_last_result(self) -> Optional[AgentResult]:
        """Get the last execution result"""
        return self.execution_history[-1] if self.execution_history else None

    def reset(self):
        """Reset agent to initial state"""
        self.status = AgentStatus.IDLE
        self.execution_history.clear()
        self.logger.info(f"Agent {self.name} reset to initial state")

    def configure(self, config: Dict[str, Any]):
        """Update agent configuration"""
        self.config.update(config)
        self.logger.info(f"Agent {self.name} configuration updated")

    def get_config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return self.config.copy()

    def get_statistics(self) -> Dict[str, Any]:
        """Get agent execution statistics"""
        if not self.execution_history:
            return {
                "total_executions": 0,
                "success_rate": 0.0,
                "average_execution_time": 0.0
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
            "current_status": self.status.value
        }

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, status={self.status.value})"

    def __repr__(self) -> str:
        return self.__str__()