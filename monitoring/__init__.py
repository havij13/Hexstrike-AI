# monitoring/__init__.py
"""
HexStrike AI Monitoring Module

This module provides monitoring and observability infrastructure including:
- Grafana dashboard setup and management
- Prometheus metrics collection
- Health checks and alerting
- Performance monitoring
"""

from .grafana_setup import GrafanaSetup
from .health_checks import HealthChecker
from .metrics import MetricsCollector

__version__ = "1.0.0"
__all__ = [
    "GrafanaSetup",
    "HealthChecker", 
    "MetricsCollector"
]