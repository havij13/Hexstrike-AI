# monitoring/alert_manager.py
"""
Alert management system for HexStrike AI monitoring infrastructure
Handles alert rules, notification channels, and escalation policies
"""
import os
import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Alert:
    """Alert data structure"""
    name: str
    severity: AlertSeverity
    message: str
    description: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    timestamp: datetime
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert alert to dictionary"""
        return {
            'name': self.name,
            'severity': self.severity.value,
            'message': self.message,
            'description': self.description,
            'labels': self.labels,
            'annotations': self.annotations,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }


class AlertManager:
    """Main alert management system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.active_alerts: Dict[str, Alert] = {}
        self.alert_history: List[Alert] = []
    
    async def fire_alert(self, alert: Alert):
        """Fire a new alert"""
        alert_key = f"{alert.name}_{hash(str(alert.labels))}"
        
        # Check if this is a duplicate alert
        if alert_key in self.active_alerts:
            self.logger.debug(f"Alert {alert.name} already active, skipping")
            return
        
        # Add to active alerts
        self.active_alerts[alert_key] = alert
        self.alert_history.append(alert)
        
        self.logger.warning(f"Alert fired: {alert.name} ({alert.severity.value})")
    
    async def resolve_alert(self, alert_name: str, labels: Dict[str, str] = None):
        """Resolve an active alert"""
        alert_key = f"{alert_name}_{hash(str(labels or {}))}"
        
        if alert_key in self.active_alerts:
            alert = self.active_alerts[alert_key]
            alert.resolved = True
            alert.resolved_at = datetime.utcnow()
            
            del self.active_alerts[alert_key]
            
            self.logger.info(f"Alert resolved: {alert.name}")
    
    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get all active alerts"""
        return [alert.to_dict() for alert in self.active_alerts.values()]
    
    def get_alert_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get alert history"""
        return [alert.to_dict() for alert in self.alert_history[-limit:]]


# Global alert manager instance
alert_manager = AlertManager()