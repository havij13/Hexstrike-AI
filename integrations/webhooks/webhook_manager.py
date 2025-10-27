#!/usr/bin/env python3
"""
HexStrike AI - Webhook Integration Manager
Real-time notifications and event-driven integrations
"""

import asyncio
import json
import logging
import hmac
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
import aiohttp
from urllib.parse import urljoin

@dataclass
class WebhookEndpoint:
    """Webhook endpoint configuration"""
    name: str
    url: str
    secret: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)
    events: List[str] = field(default_factory=list)
    active: bool = True
    retry_count: int = 3
    timeout: int = 30

class WebhookManager:
    """Advanced webhook management for real-time integrations"""
    
    def __init__(self):
        self.endpoints: Dict[str, WebhookEndpoint] = {}
        self.session = None
        self.logger = logging.getLogger(__name__)
        self.event_handlers: Dict[str, List[Callable]] = {}
        
    async def initialize(self):
        """Initialize webhook manager"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        self.logger.info("Webhook Manager initialized")
        
    async def close(self):
        """Close webhook manager"""
        if self.session:
            await self.session.close()
            
    def register_endpoint(self, endpoint: WebhookEndpoint):
        """Register webhook endpoint"""
        self.endpoints[endpoint.name] = endpoint
        self.logger.info(f"Registered webhook endpoint: {endpoint.name}")
        
    async def send_webhook(self, event_type: str, data: Dict[str, Any], 
                          endpoint_name: Optional[str] = None) -> Dict[str, bool]:
        """Send webhook to registered endpoints"""
        results = {}
        
        # Determine which endpoints to send to
        target_endpoints = []
        if endpoint_name:
            if endpoint_name in self.endpoints:
                target_endpoints = [self.endpoints[endpoint_name]]
        else:
            target_endpoints = [
                ep for ep in self.endpoints.values() 
                if ep.active and (not ep.events or event_type in ep.events)
            ]
            
        # Send to all target endpoints
        tasks = []
        for endpoint in target_endpoints:
            task = self._send_to_endpoint(endpoint, event_type, data)
            tasks.append(task)
            
        if tasks:
            endpoint_results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(endpoint_results):
                endpoint_name = target_endpoints[i].name
                results[endpoint_name] = not isinstance(result, Exception) and result
                
        return results    
    
    async def _send_to_endpoint(self, endpoint: WebhookEndpoint, 
                               event_type: str, data: Dict[str, Any]) -> bool:
        """Send webhook to specific endpoint with retry logic"""
        payload = {
            'event_type': event_type,
            'timestamp': datetime.utcnow().isoformat(),
            'data': data,
            'source': 'hexstrike-ai'
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'HexStrike-AI-Webhook/6.0',
            **endpoint.headers
        }
        
        # Add signature if secret is provided
        if endpoint.secret:
            signature = self._generate_signature(json.dumps(payload), endpoint.secret)
            headers['X-HexStrike-Signature'] = signature
            
        for attempt in range(endpoint.retry_count):
            try:
                async with self.session.post(
                    endpoint.url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=endpoint.timeout)
                ) as response:
                    if 200 <= response.status < 300:
                        self.logger.info(f"Webhook sent successfully to {endpoint.name}")
                        return True
                    else:
                        self.logger.warning(
                            f"Webhook failed to {endpoint.name}: {response.status}"
                        )
                        
            except Exception as e:
                self.logger.error(
                    f"Webhook error to {endpoint.name} (attempt {attempt + 1}): {str(e)}"
                )
                
            # Wait before retry (exponential backoff)
            if attempt < endpoint.retry_count - 1:
                await asyncio.sleep(2 ** attempt)
                
        return False
        
    def _generate_signature(self, payload: str, secret: str) -> str:
        """Generate HMAC signature for webhook payload"""
        signature = hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return f"sha256={signature}"
        
    # Event-specific webhook methods
    async def send_vulnerability_alert(self, vulnerability: Dict[str, Any]):
        """Send vulnerability discovery webhook"""
        await self.send_webhook('vulnerability_found', vulnerability)
        
    async def send_scan_complete(self, scan_result: Dict[str, Any]):
        """Send scan completion webhook"""
        await self.send_webhook('scan_completed', scan_result)
        
    async def send_critical_alert(self, alert_data: Dict[str, Any]):
        """Send critical security alert"""
        await self.send_webhook('critical_alert', alert_data)
        
    async def send_threat_detected(self, threat_data: Dict[str, Any]):
        """Send threat detection webhook"""
        await self.send_webhook('threat_detected', threat_data)

# Predefined webhook configurations for popular services
class WebhookTemplates:
    """Predefined webhook templates for popular services"""
    
    @staticmethod
    def slack_webhook(webhook_url: str, channel: str = "#security") -> WebhookEndpoint:
        """Create Slack webhook endpoint"""
        return WebhookEndpoint(
            name="slack",
            url=webhook_url,
            headers={"Content-Type": "application/json"},
            events=["vulnerability_found", "critical_alert", "scan_completed"]
        )
        
    @staticmethod
    def teams_webhook(webhook_url: str) -> WebhookEndpoint:
        """Create Microsoft Teams webhook endpoint"""
        return WebhookEndpoint(
            name="teams",
            url=webhook_url,
            headers={"Content-Type": "application/json"},
            events=["vulnerability_found", "critical_alert"]
        )
        
    @staticmethod
    def discord_webhook(webhook_url: str) -> WebhookEndpoint:
        """Create Discord webhook endpoint"""
        return WebhookEndpoint(
            name="discord",
            url=webhook_url,
            headers={"Content-Type": "application/json"},
            events=["vulnerability_found", "scan_completed"]
        )
        
    @staticmethod
    def pagerduty_webhook(integration_key: str) -> WebhookEndpoint:
        """Create PagerDuty webhook endpoint"""
        return WebhookEndpoint(
            name="pagerduty",
            url="https://events.pagerduty.com/v2/enqueue",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Token token={integration_key}"
            },
            events=["critical_alert", "vulnerability_found"]
        )

# Example usage
async def main():
    """Example webhook manager usage"""
    manager = WebhookManager()
    await manager.initialize()
    
    try:
        # Register Slack webhook
        slack_endpoint = WebhookTemplates.slack_webhook(
            "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
        )
        manager.register_endpoint(slack_endpoint)
        
        # Send test vulnerability alert
        vulnerability = {
            "severity": "critical",
            "title": "SQL Injection Vulnerability",
            "target": "web.company.com",
            "cvss_score": 9.8
        }
        
        results = await manager.send_vulnerability_alert(vulnerability)
        print(f"Webhook results: {results}")
        
    finally:
        await manager.close()

if __name__ == "__main__":
    asyncio.run(main())