#!/usr/bin/env python3
"""
HexStrike AI - Splunk SIEM Integration
Real-time log forwarding and security event correlation
"""

import json
import logging
import requests
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import asyncio
import aiohttp
from urllib.parse import urljoin

@dataclass
class SplunkConfig:
    """Splunk configuration settings"""
    host: str
    port: int = 8088
    token: str = ""
    index: str = "hexstrike"
    source: str = "hexstrike-ai"
    sourcetype: str = "json"
    ssl_verify: bool = True
    timeout: int = 30

class SplunkIntegration:
    """Advanced Splunk integration for HexStrike AI"""
    
    def __init__(self, config: SplunkConfig):
        self.config = config
        self.base_url = f"{'https' if config.ssl_verify else 'http'}://{config.host}:{config.port}"
        self.hec_url = urljoin(self.base_url, "/services/collector/event")
        self.session = None
        self.logger = logging.getLogger(__name__)
        
    async def initialize(self):
        """Initialize async HTTP session"""
        connector = aiohttp.TCPConnector(ssl=self.config.ssl_verify)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=self.config.timeout),
            headers={
                'Authorization': f'Splunk {self.config.token}',
                'Content-Type': 'application/json'
            }
        )
        
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            
    async def send_event(self, event_data: Dict[str, Any], 
                        event_type: str = "security_scan") -> bool:
        """Send security event to Splunk"""
        try:
            splunk_event = {
                "time": int(time.time()),
                "host": "hexstrike-ai",
                "source": self.config.source,
                "sourcetype": self.config.sourcetype,
                "index": self.config.index,
                "event": {
                    "event_type": event_type,
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": event_data,
                    "severity": event_data.get("severity", "info"),
                    "tool": event_data.get("tool_name", "unknown"),
                    "target": event_data.get("target", "unknown")
                }
            }
            
            async with self.session.post(self.hec_url, json=splunk_event) as response:
                if response.status == 200:
                    self.logger.info(f"Successfully sent event to Splunk: {event_type}")
                    return True
                else:
                    error_text = await response.text()
                    self.logger.error(f"Failed to send event to Splunk: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error sending event to Splunk: {str(e)}")
            return False
            
    async def send_vulnerability(self, vulnerability: Dict[str, Any]) -> bool:
        """Send vulnerability finding to Splunk"""
        vuln_event = {
            "vulnerability_id": vulnerability.get("id"),
            "severity": vulnerability.get("severity", "unknown"),
            "cvss_score": vulnerability.get("cvss_score", 0),
            "cve_id": vulnerability.get("cve_id"),
            "description": vulnerability.get("description"),
            "target": vulnerability.get("target"),
            "port": vulnerability.get("port"),
            "service": vulnerability.get("service"),
            "tool_used": vulnerability.get("tool_name"),
            "remediation": vulnerability.get("remediation"),
            "references": vulnerability.get("references", []),
            "risk_score": self._calculate_risk_score(vulnerability)
        }
        
        return await self.send_event(vuln_event, "vulnerability_found")
        
    async def send_scan_result(self, scan_result: Dict[str, Any]) -> bool:
        """Send scan result to Splunk"""
        scan_event = {
            "scan_id": scan_result.get("scan_id"),
            "tool_name": scan_result.get("tool_name"),
            "target": scan_result.get("target"),
            "scan_type": scan_result.get("scan_type"),
            "start_time": scan_result.get("start_time"),
            "end_time": scan_result.get("end_time"),
            "duration": scan_result.get("duration"),
            "status": scan_result.get("status"),
            "findings_count": len(scan_result.get("findings", [])),
            "critical_count": len([f for f in scan_result.get("findings", []) if f.get("severity") == "critical"]),
            "high_count": len([f for f in scan_result.get("findings", []) if f.get("severity") == "high"]),
            "command_executed": scan_result.get("command"),
            "exit_code": scan_result.get("exit_code")
        }
        
        return await self.send_event(scan_event, "scan_completed")
        
    async def send_threat_intelligence(self, ioc_data: Dict[str, Any]) -> bool:
        """Send threat intelligence IOC to Splunk"""
        ioc_event = {
            "ioc_type": ioc_data.get("type"),
            "ioc_value": ioc_data.get("value"),
            "threat_type": ioc_data.get("threat_type"),
            "confidence": ioc_data.get("confidence"),
            "source": ioc_data.get("source"),
            "first_seen": ioc_data.get("first_seen"),
            "last_seen": ioc_data.get("last_seen"),
            "tags": ioc_data.get("tags", []),
            "malware_family": ioc_data.get("malware_family"),
            "campaign": ioc_data.get("campaign")
        }
        
        return await self.send_event(ioc_event, "threat_intelligence")
        
    async def create_notable_event(self, event_data: Dict[str, Any]) -> bool:
        """Create notable event in Splunk ES"""
        notable_event = {
            "rule_name": f"HexStrike AI - {event_data.get('event_type', 'Security Alert')}",
            "rule_title": event_data.get("title", "Security Finding"),
            "security_domain": "endpoint",
            "severity": event_data.get("severity", "medium"),
            "urgency": self._map_severity_to_urgency(event_data.get("severity")),
            "owner": "hexstrike-ai",
            "status": "new",
            "disposition": "undecided",
            "event_id": event_data.get("event_id"),
            "src": event_data.get("target"),
            "dest": event_data.get("target"),
            "signature": event_data.get("signature"),
            "description": event_data.get("description")
        }
        
        return await self.send_event(notable_event, "notable_event")
        
    def _calculate_risk_score(self, vulnerability: Dict[str, Any]) -> float:
        """Calculate risk score based on vulnerability data"""
        base_score = vulnerability.get("cvss_score", 0)
        severity_multiplier = {
            "critical": 1.0,
            "high": 0.8,
            "medium": 0.6,
            "low": 0.4,
            "info": 0.2
        }
        
        severity = vulnerability.get("severity", "info").lower()
        multiplier = severity_multiplier.get(severity, 0.5)
        
        # Consider exploitability and impact
        if vulnerability.get("exploitable", False):
            multiplier *= 1.2
            
        if vulnerability.get("public_exploit", False):
            multiplier *= 1.3
            
        return min(base_score * multiplier, 10.0)
        
    def _map_severity_to_urgency(self, severity: str) -> str:
        """Map vulnerability severity to Splunk urgency"""
        mapping = {
            "critical": "high",
            "high": "high",
            "medium": "medium",
            "low": "low",
            "info": "low"
        }
        return mapping.get(severity.lower(), "medium")

class SplunkSearchAPI:
    """Splunk Search API integration for querying security data"""
    
    def __init__(self, config: SplunkConfig):
        self.config = config
        self.base_url = f"{'https' if config.ssl_verify else 'http'}://{config.host}:8089"
        self.session = None
        
    async def initialize(self):
        """Initialize search API session"""
        connector = aiohttp.TCPConnector(ssl=self.config.ssl_verify)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=self.config.timeout)
        )
        
    async def search_vulnerabilities(self, target: str, 
                                   time_range: str = "-24h") -> List[Dict[str, Any]]:
        """Search for vulnerabilities related to a target"""
        search_query = f'''
        search index={self.config.index} event_type="vulnerability_found" target="{target}"
        | eval risk_category=case(
            risk_score>=8, "Critical",
            risk_score>=6, "High", 
            risk_score>=4, "Medium",
            1=1, "Low"
        )
        | stats count by severity, risk_category, cve_id
        | sort -count
        '''
        
        return await self._execute_search(search_query, time_range)
        
    async def get_threat_trends(self, time_range: str = "-7d") -> List[Dict[str, Any]]:
        """Get threat trends over time"""
        search_query = f'''
        search index={self.config.index} event_type="vulnerability_found"
        | timechart span=1d count by severity
        | fillnull value=0
        '''
        
        return await self._execute_search(search_query, time_range)
        
    async def _execute_search(self, query: str, time_range: str) -> List[Dict[str, Any]]:
        """Execute Splunk search query"""
        try:
            # Create search job
            search_data = {
                'search': query,
                'earliest_time': time_range,
                'latest_time': 'now',
                'output_mode': 'json'
            }
            
            auth = aiohttp.BasicAuth(self.config.token.split(':')[0], 
                                   self.config.token.split(':')[1])
            
            async with self.session.post(
                f"{self.base_url}/services/search/jobs",
                data=search_data,
                auth=auth
            ) as response:
                if response.status == 201:
                    job_data = await response.json()
                    job_id = job_data['sid']
                    
                    # Wait for job completion and get results
                    return await self._get_search_results(job_id, auth)
                else:
                    return []
                    
        except Exception as e:
            logging.error(f"Error executing Splunk search: {str(e)}")
            return []
            
    async def _get_search_results(self, job_id: str, auth) -> List[Dict[str, Any]]:
        """Get results from completed search job"""
        try:
            # Poll for job completion
            for _ in range(30):  # Wait up to 30 seconds
                async with self.session.get(
                    f"{self.base_url}/services/search/jobs/{job_id}",
                    params={'output_mode': 'json'},
                    auth=auth
                ) as response:
                    if response.status == 200:
                        job_status = await response.json()
                        if job_status['entry'][0]['content']['isDone']:
                            break
                            
                await asyncio.sleep(1)
                
            # Get results
            async with self.session.get(
                f"{self.base_url}/services/search/jobs/{job_id}/results",
                params={'output_mode': 'json', 'count': 1000},
                auth=auth
            ) as response:
                if response.status == 200:
                    results = await response.json()
                    return results.get('results', [])
                    
        except Exception as e:
            logging.error(f"Error getting search results: {str(e)}")
            
        return []

# Example usage and integration
async def main():
    """Example usage of Splunk integration"""
    config = SplunkConfig(
        host="splunk.company.com",
        token="your-hec-token-here",
        index="security",
        ssl_verify=True
    )
    
    splunk = SplunkIntegration(config)
    await splunk.initialize()
    
    try:
        # Send vulnerability
        vulnerability = {
            "id": "VULN-001",
            "severity": "critical",
            "cvss_score": 9.8,
            "cve_id": "CVE-2024-1234",
            "description": "Remote code execution vulnerability",
            "target": "192.168.1.100",
            "port": 80,
            "service": "http",
            "tool_name": "nuclei"
        }
        
        await splunk.send_vulnerability(vulnerability)
        
        # Send scan result
        scan_result = {
            "scan_id": "SCAN-001",
            "tool_name": "nmap",
            "target": "192.168.1.0/24",
            "scan_type": "network_discovery",
            "status": "completed",
            "findings": [vulnerability]
        }
        
        await splunk.send_scan_result(scan_result)
        
    finally:
        await splunk.close()

if __name__ == "__main__":
    asyncio.run(main())