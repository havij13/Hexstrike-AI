#!/usr/bin/env python3
"""
HexStrike AI - Jira Integration
Automated ticket creation and vulnerability management
"""

import json
import logging
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import base64
from urllib.parse import urljoin

@dataclass
class JiraConfig:
    """Jira configuration settings"""
    url: str
    username: str
    api_token: str
    project_key: str
    issue_type: str = "Bug"
    priority_mapping: Dict[str, str] = None
    custom_fields: Dict[str, str] = None
    
    def __post_init__(self):
        if self.priority_mapping is None:
            self.priority_mapping = {
                "critical": "Highest",
                "high": "High", 
                "medium": "Medium",
                "low": "Low",
                "info": "Lowest"
            }
        if self.custom_fields is None:
            self.custom_fields = {}

class JiraIntegration:
    """Advanced Jira integration for vulnerability management"""
    
    def __init__(self, config: JiraConfig):
        self.config = config
        self.base_url = config.url.rstrip('/')
        self.api_url = urljoin(self.base_url, '/rest/api/3/')
        self.session = None
        self.logger = logging.getLogger(__name__)
        
        # Create auth header
        auth_string = f"{config.username}:{config.api_token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        self.auth_header = f"Basic {auth_b64}"
        
    async def initialize(self):
        """Initialize async HTTP session"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'Authorization': self.auth_header,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )
        
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            
    async def create_vulnerability_ticket(self, vulnerability: Dict[str, Any]) -> Optional[str]:
        """Create Jira ticket for vulnerability"""
        try:
            # Prepare ticket data
            ticket_data = self._prepare_vulnerability_ticket(vulnerability)
            
            # Create ticket
            async with self.session.post(
                urljoin(self.api_url, 'issue'),
                json=ticket_data
            ) as response:
                if response.status == 201:
                    result = await response.json()
                    ticket_key = result['key']
                    self.logger.info(f"Created Jira ticket: {ticket_key}")
                    
                    # Add vulnerability details as comment
                    await self._add_vulnerability_comment(ticket_key, vulnerability)
                    
                    # Set labels and components
                    await self._update_ticket_metadata(ticket_key, vulnerability)
                    
                    return ticket_key
                else:
                    error_text = await response.text()
                    self.logger.error(f"Failed to create Jira ticket: {response.status} - {error_text}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error creating Jira ticket: {str(e)}")
            return None
            
    async def create_scan_summary_ticket(self, scan_result: Dict[str, Any]) -> Optional[str]:
        """Create summary ticket for scan results"""
        try:
            summary = f"Security Scan Results - {scan_result.get('target', 'Unknown Target')}"
            
            # Count vulnerabilities by severity
            findings = scan_result.get('findings', [])
            severity_counts = {}
            for finding in findings:
                severity = finding.get('severity', 'unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
                
            # Determine overall priority
            if severity_counts.get('critical', 0) > 0:
                priority = "Highest"
            elif severity_counts.get('high', 0) > 0:
                priority = "High"
            elif severity_counts.get('medium', 0) > 0:
                priority = "Medium"
            else:
                priority = "Low"
                
            description = self._generate_scan_description(scan_result, severity_counts)
            
            ticket_data = {
                "fields": {
                    "project": {"key": self.config.project_key},
                    "summary": summary,
                    "description": {
                        "type": "doc",
                        "version": 1,
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": description
                                    }
                                ]
                            }
                        ]
                    },
                    "issuetype": {"name": self.config.issue_type},
                    "priority": {"name": priority},
                    "labels": [
                        "hexstrike-ai",
                        "security-scan",
                        scan_result.get('tool_name', 'unknown').replace(' ', '-').lower()
                    ]
                }
            }
            
            # Add custom fields
            for field_id, value in self.config.custom_fields.items():
                ticket_data["fields"][field_id] = value
                
            async with self.session.post(
                urljoin(self.api_url, 'issue'),
                json=ticket_data
            ) as response:
                if response.status == 201:
                    result = await response.json()
                    ticket_key = result['key']
                    self.logger.info(f"Created scan summary ticket: {ticket_key}")
                    
                    # Create individual vulnerability tickets and link them
                    for vulnerability in findings:
                        if vulnerability.get('severity') in ['critical', 'high']:
                            vuln_ticket = await self.create_vulnerability_ticket(vulnerability)
                            if vuln_ticket:
                                await self._link_tickets(ticket_key, vuln_ticket, "relates to")
                                
                    return ticket_key
                else:
                    error_text = await response.text()
                    self.logger.error(f"Failed to create scan summary ticket: {response.status} - {error_text}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"Error creating scan summary ticket: {str(e)}")
            return None
            
    async def update_ticket_status(self, ticket_key: str, status: str) -> bool:
        """Update ticket status"""
        try:
            # Get available transitions
            async with self.session.get(
                urljoin(self.api_url, f'issue/{ticket_key}/transitions')
            ) as response:
                if response.status == 200:
                    transitions = await response.json()
                    
                    # Find transition ID for desired status
                    transition_id = None
                    for transition in transitions['transitions']:
                        if transition['to']['name'].lower() == status.lower():
                            transition_id = transition['id']
                            break
                            
                    if transition_id:
                        # Execute transition
                        transition_data = {
                            "transition": {"id": transition_id}
                        }
                        
                        async with self.session.post(
                            urljoin(self.api_url, f'issue/{ticket_key}/transitions'),
                            json=transition_data
                        ) as trans_response:
                            if trans_response.status == 204:
                                self.logger.info(f"Updated ticket {ticket_key} status to {status}")
                                return True
                            else:
                                error_text = await trans_response.text()
                                self.logger.error(f"Failed to update ticket status: {trans_response.status} - {error_text}")
                                return False
                    else:
                        self.logger.warning(f"Status '{status}' not available for ticket {ticket_key}")
                        return False
                else:
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error updating ticket status: {str(e)}")
            return False
            
    async def add_comment(self, ticket_key: str, comment: str) -> bool:
        """Add comment to ticket"""
        try:
            comment_data = {
                "body": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": comment
                                }
                            ]
                        }
                    ]
                }
            }
            
            async with self.session.post(
                urljoin(self.api_url, f'issue/{ticket_key}/comment'),
                json=comment_data
            ) as response:
                if response.status == 201:
                    self.logger.info(f"Added comment to ticket {ticket_key}")
                    return True
                else:
                    error_text = await response.text()
                    self.logger.error(f"Failed to add comment: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error adding comment: {str(e)}")
            return False
            
    def _prepare_vulnerability_ticket(self, vulnerability: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare Jira ticket data for vulnerability"""
        severity = vulnerability.get('severity', 'medium').lower()
        priority = self.config.priority_mapping.get(severity, 'Medium')
        
        summary = f"[{severity.upper()}] {vulnerability.get('title', 'Security Vulnerability')} - {vulnerability.get('target', 'Unknown')}"
        
        description = f"""
**Vulnerability Details:**
- **Target:** {vulnerability.get('target', 'Unknown')}
- **Severity:** {severity.upper()}
- **CVSS Score:** {vulnerability.get('cvss_score', 'N/A')}
- **CVE ID:** {vulnerability.get('cve_id', 'N/A')}
- **Tool Used:** {vulnerability.get('tool_name', 'Unknown')}

**Description:**
{vulnerability.get('description', 'No description available')}

**Impact:**
{vulnerability.get('impact', 'Impact assessment pending')}

**Remediation:**
{vulnerability.get('remediation', 'Remediation steps to be determined')}

**References:**
{chr(10).join(vulnerability.get('references', []))}

**Discovery Information:**
- **Discovered:** {datetime.utcnow().isoformat()}
- **Port:** {vulnerability.get('port', 'N/A')}
- **Service:** {vulnerability.get('service', 'N/A')}
- **Protocol:** {vulnerability.get('protocol', 'N/A')}
"""
        
        ticket_data = {
            "fields": {
                "project": {"key": self.config.project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {"name": self.config.issue_type},
                "priority": {"name": priority},
                "labels": [
                    "hexstrike-ai",
                    "vulnerability",
                    severity,
                    vulnerability.get('tool_name', 'unknown').replace(' ', '-').lower()
                ]
            }
        }
        
        # Add CVE as component if available
        if vulnerability.get('cve_id'):
            ticket_data["fields"]["labels"].append(vulnerability['cve_id'].lower())
            
        # Add custom fields
        for field_id, value in self.config.custom_fields.items():
            ticket_data["fields"][field_id] = value
            
        return ticket_data
        
    def _generate_scan_description(self, scan_result: Dict[str, Any], 
                                 severity_counts: Dict[str, int]) -> str:
        """Generate description for scan summary ticket"""
        target = scan_result.get('target', 'Unknown Target')
        tool = scan_result.get('tool_name', 'Unknown Tool')
        scan_type = scan_result.get('scan_type', 'Security Scan')
        
        description = f"""
**Scan Summary Report**

**Target:** {target}
**Tool Used:** {tool}
**Scan Type:** {scan_type}
**Scan Date:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
**Duration:** {scan_result.get('duration', 'Unknown')}

**Findings Summary:**
"""
        
        total_findings = sum(severity_counts.values())
        description += f"- **Total Findings:** {total_findings}\n"
        
        for severity in ['critical', 'high', 'medium', 'low', 'info']:
            count = severity_counts.get(severity, 0)
            if count > 0:
                description += f"- **{severity.title()}:** {count}\n"
                
        if scan_result.get('command'):
            description += f"\n**Command Executed:**\n```\n{scan_result['command']}\n```\n"
            
        description += f"\n**Status:** {scan_result.get('status', 'Unknown')}"
        
        if total_findings > 0:
            description += "\n\n**Next Steps:**\n"
            description += "1. Review individual vulnerability tickets\n"
            description += "2. Prioritize remediation based on severity\n"
            description += "3. Assign tickets to appropriate teams\n"
            description += "4. Schedule follow-up scans after remediation\n"
            
        return description
        
    async def _add_vulnerability_comment(self, ticket_key: str, 
                                       vulnerability: Dict[str, Any]) -> bool:
        """Add detailed vulnerability information as comment"""
        technical_details = f"""
**Technical Details:**

**Raw Output:**
```
{vulnerability.get('raw_output', 'No raw output available')}
```

**Additional Information:**
- **Plugin ID:** {vulnerability.get('plugin_id', 'N/A')}
- **Risk Factor:** {vulnerability.get('risk_factor', 'N/A')}
- **Solution:** {vulnerability.get('solution', 'N/A')}
- **See Also:** {vulnerability.get('see_also', 'N/A')}

**Affected Assets:**
{json.dumps(vulnerability.get('affected_assets', []), indent=2)}
"""
        
        return await self.add_comment(ticket_key, technical_details)
        
    async def _update_ticket_metadata(self, ticket_key: str, 
                                    vulnerability: Dict[str, Any]) -> bool:
        """Update ticket with additional metadata"""
        try:
            # Add security-specific labels
            additional_labels = []
            
            if vulnerability.get('exploitable'):
                additional_labels.append('exploitable')
                
            if vulnerability.get('public_exploit'):
                additional_labels.append('public-exploit')
                
            if vulnerability.get('patch_available'):
                additional_labels.append('patch-available')
                
            if additional_labels:
                update_data = {
                    "fields": {
                        "labels": additional_labels
                    }
                }
                
                async with self.session.put(
                    urljoin(self.api_url, f'issue/{ticket_key}'),
                    json=update_data
                ) as response:
                    return response.status == 204
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating ticket metadata: {str(e)}")
            return False
            
    async def _link_tickets(self, parent_key: str, child_key: str, 
                          link_type: str = "relates to") -> bool:
        """Link two tickets together"""
        try:
            link_data = {
                "type": {"name": link_type},
                "inwardIssue": {"key": parent_key},
                "outwardIssue": {"key": child_key}
            }
            
            async with self.session.post(
                urljoin(self.api_url, 'issueLink'),
                json=link_data
            ) as response:
                if response.status == 201:
                    self.logger.info(f"Linked tickets: {parent_key} -> {child_key}")
                    return True
                else:
                    error_text = await response.text()
                    self.logger.error(f"Failed to link tickets: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error linking tickets: {str(e)}")
            return False

# Example usage
async def main():
    """Example usage of Jira integration"""
    config = JiraConfig(
        url="https://company.atlassian.net",
        username="security@company.com",
        api_token="your-api-token-here",
        project_key="SEC",
        issue_type="Security Issue",
        custom_fields={
            "customfield_10001": "HexStrike AI",  # Source field
            "customfield_10002": {"value": "External"}  # Security Type field
        }
    )
    
    jira = JiraIntegration(config)
    await jira.initialize()
    
    try:
        # Create vulnerability ticket
        vulnerability = {
            "title": "SQL Injection Vulnerability",
            "severity": "high",
            "cvss_score": 8.5,
            "cve_id": "CVE-2024-1234",
            "description": "SQL injection vulnerability in login form",
            "target": "web.company.com",
            "port": 443,
            "service": "https",
            "tool_name": "sqlmap",
            "remediation": "Use parameterized queries",
            "references": ["https://owasp.org/www-community/attacks/SQL_Injection"]
        }
        
        ticket_key = await jira.create_vulnerability_ticket(vulnerability)
        if ticket_key:
            print(f"Created ticket: {ticket_key}")
            
    finally:
        await jira.close()

if __name__ == "__main__":
    asyncio.run(main())