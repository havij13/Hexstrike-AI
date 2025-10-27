#!/usr/bin/env python3
"""
HexStrike AI - Advanced Threat Hunting Agent
Proactive threat detection using AI and machine learning
"""

import asyncio
import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import requests
import aiohttp
import hashlib
import re
from collections import defaultdict, Counter

@dataclass
class ThreatIndicator:
    """Threat indicator data structure"""
    ioc_type: str  # ip, domain, hash, url, etc.
    value: str
    confidence: float
    source: str
    first_seen: datetime
    last_seen: datetime
    threat_types: List[str] = field(default_factory=list)
    malware_families: List[str] = field(default_factory=list)
    campaigns: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

@dataclass
class ThreatHunt:
    """Threat hunting session data"""
    hunt_id: str
    name: str
    description: str
    hypothesis: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "active"  # active, completed, paused
    findings: List[Dict[str, Any]] = field(default_factory=list)
    iocs_discovered: List[ThreatIndicator] = field(default_factory=list)
    confidence_score: float = 0.0

class ThreatHuntingAgent:
    """Advanced AI-powered threat hunting agent"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.session = None
        
        # ML models for anomaly detection
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.dbscan = DBSCAN(eps=0.5, min_samples=5)
        
        # Threat intelligence sources
        self.ti_sources = {
            'virustotal': config.get('virustotal_api_key'),
            'abuseipdb': config.get('abuseipdb_api_key'),
            'otx': config.get('otx_api_key'),
            'misp': config.get('misp_url')
        }
        
        # Active hunts
        self.active_hunts: Dict[str, ThreatHunt] = {}
        
        # IOC cache
        self.ioc_cache: Dict[str, ThreatIndicator] = {}
        
    async def initialize(self):
        """Initialize the threat hunting agent"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        
        # Load existing IOCs and threat intelligence
        await self._load_threat_intelligence()
        
        self.logger.info("Threat Hunting Agent initialized")
        
    async def close(self):
        """Close the agent and cleanup resources"""
        if self.session:
            await self.session.close()
            
    async def start_hunt(self, hunt_config: Dict[str, Any]) -> str:
        """Start a new threat hunting session"""
        hunt_id = hashlib.md5(
            f"{hunt_config['name']}{datetime.utcnow()}".encode()
        ).hexdigest()[:12]
        
        hunt = ThreatHunt(
            hunt_id=hunt_id,
            name=hunt_config['name'],
            description=hunt_config.get('description', ''),
            hypothesis=hunt_config.get('hypothesis', ''),
            start_time=datetime.utcnow()
        )
        
        self.active_hunts[hunt_id] = hunt
        
        self.logger.info(f"Started threat hunt: {hunt_id} - {hunt.name}")
        
        # Execute hunt based on type
        hunt_type = hunt_config.get('type', 'behavioral_analysis')
        
        if hunt_type == 'behavioral_analysis':
            await self._hunt_behavioral_anomalies(hunt, hunt_config)
        elif hunt_type == 'ioc_hunting':
            await self._hunt_known_iocs(hunt, hunt_config)
        elif hunt_type == 'lateral_movement':
            await self._hunt_lateral_movement(hunt, hunt_config)
        elif hunt_type == 'data_exfiltration':
            await self._hunt_data_exfiltration(hunt, hunt_config)
        elif hunt_type == 'persistence_mechanisms':
            await self._hunt_persistence(hunt, hunt_config)
        else:
            await self._hunt_generic_threats(hunt, hunt_config)
            
        return hunt_id
        
    async def _hunt_behavioral_anomalies(self, hunt: ThreatHunt, 
                                       config: Dict[str, Any]):
        """Hunt for behavioral anomalies using ML"""
        try:
            # Collect network traffic data
            network_data = await self._collect_network_data(config)
            
            if not network_data:
                self.logger.warning("No network data available for behavioral analysis")
                return
                
            # Feature extraction
            features = self._extract_behavioral_features(network_data)
            
            # Anomaly detection
            anomalies = self._detect_anomalies(features)
            
            # Analyze anomalies
            for anomaly in anomalies:
                finding = await self._analyze_anomaly(anomaly, network_data)
                if finding:
                    hunt.findings.append(finding)
                    
                    # Extract IOCs from anomaly
                    iocs = self._extract_iocs_from_anomaly(anomaly)
                    hunt.iocs_discovered.extend(iocs)
                    
            # Update confidence score
            hunt.confidence_score = self._calculate_hunt_confidence(hunt)
            
            self.logger.info(f"Behavioral analysis complete: {len(hunt.findings)} findings")
            
        except Exception as e:
            self.logger.error(f"Error in behavioral anomaly hunting: {str(e)}")
            
    async def _hunt_known_iocs(self, hunt: ThreatHunt, config: Dict[str, Any]):
        """Hunt for known IOCs in network traffic and logs"""
        try:
            # Get IOCs to hunt for
            target_iocs = config.get('iocs', [])
            if not target_iocs:
                target_iocs = list(self.ioc_cache.keys())
                
            # Search for IOCs in various data sources
            for ioc in target_iocs:
                findings = await self._search_ioc_in_logs(ioc)
                hunt.findings.extend(findings)
                
                # Check network traffic
                network_findings = await self._search_ioc_in_network(ioc)
                hunt.findings.extend(network_findings)
                
                # DNS queries
                dns_findings = await self._search_ioc_in_dns(ioc)
                hunt.findings.extend(dns_findings)
                
            hunt.confidence_score = self._calculate_hunt_confidence(hunt)
            
            self.logger.info(f"IOC hunting complete: {len(hunt.findings)} findings")
            
        except Exception as e:
            self.logger.error(f"Error in IOC hunting: {str(e)}")
            
    async def _hunt_lateral_movement(self, hunt: ThreatHunt, 
                                   config: Dict[str, Any]):
        """Hunt for lateral movement indicators"""
        try:
            # Look for suspicious authentication patterns
            auth_anomalies = await self._detect_auth_anomalies()
            hunt.findings.extend(auth_anomalies)
            
            # Detect unusual network connections
            network_anomalies = await self._detect_lateral_network_patterns()
            hunt.findings.extend(network_anomalies)
            
            # Check for privilege escalation
            privesc_indicators = await self._detect_privilege_escalation()
            hunt.findings.extend(privesc_indicators)
            
            # Remote access tools
            rat_indicators = await self._detect_remote_access_tools()
            hunt.findings.extend(rat_indicators)
            
            hunt.confidence_score = self._calculate_hunt_confidence(hunt)
            
            self.logger.info(f"Lateral movement hunting complete: {len(hunt.findings)} findings")
            
        except Exception as e:
            self.logger.error(f"Error in lateral movement hunting: {str(e)}")
            
    async def _hunt_data_exfiltration(self, hunt: ThreatHunt, 
                                    config: Dict[str, Any]):
        """Hunt for data exfiltration indicators"""
        try:
            # Unusual data transfer patterns
            transfer_anomalies = await self._detect_data_transfer_anomalies()
            hunt.findings.extend(transfer_anomalies)
            
            # DNS tunneling
            dns_tunneling = await self._detect_dns_tunneling()
            hunt.findings.extend(dns_tunneling)
            
            # Steganography indicators
            stego_indicators = await self._detect_steganography()
            hunt.findings.extend(stego_indicators)
            
            # Cloud storage uploads
            cloud_uploads = await self._detect_suspicious_cloud_activity()
            hunt.findings.extend(cloud_uploads)
            
            hunt.confidence_score = self._calculate_hunt_confidence(hunt)
            
            self.logger.info(f"Data exfiltration hunting complete: {len(hunt.findings)} findings")
            
        except Exception as e:
            self.logger.error(f"Error in data exfiltration hunting: {str(e)}")
            
    async def _collect_network_data(self, config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Collect network traffic data for analysis"""
        # This would integrate with network monitoring tools
        # For now, return mock data structure
        return [
            {
                'timestamp': datetime.utcnow(),
                'src_ip': '192.168.1.100',
                'dst_ip': '8.8.8.8',
                'src_port': 12345,
                'dst_port': 53,
                'protocol': 'UDP',
                'bytes_sent': 64,
                'bytes_received': 128,
                'duration': 0.1
            }
        ]
        
    def _extract_behavioral_features(self, network_data: List[Dict[str, Any]]) -> np.ndarray:
        """Extract features for behavioral analysis"""
        features = []
        
        for conn in network_data:
            feature_vector = [
                conn.get('bytes_sent', 0),
                conn.get('bytes_received', 0),
                conn.get('duration', 0),
                conn.get('src_port', 0),
                conn.get('dst_port', 0),
                1 if conn.get('protocol') == 'TCP' else 0,
                1 if conn.get('protocol') == 'UDP' else 0,
                len(str(conn.get('dst_ip', ''))),  # IP string length as feature
            ]
            features.append(feature_vector)
            
        return np.array(features)
        
    def _detect_anomalies(self, features: np.ndarray) -> List[Dict[str, Any]]:
        """Detect anomalies using machine learning"""
        if len(features) < 10:  # Need minimum samples
            return []
            
        # Normalize features
        features_scaled = self.scaler.fit_transform(features)
        
        # Detect anomalies
        anomaly_scores = self.isolation_forest.fit_predict(features_scaled)
        
        # Cluster analysis
        clusters = self.dbscan.fit_predict(features_scaled)
        
        anomalies = []
        for i, (score, cluster) in enumerate(zip(anomaly_scores, clusters)):
            if score == -1:  # Anomaly detected
                anomalies.append({
                    'index': i,
                    'anomaly_score': score,
                    'cluster': cluster,
                    'features': features[i],
                    'confidence': abs(score) * 0.8  # Convert to confidence
                })
                
        return anomalies
        
    async def _analyze_anomaly(self, anomaly: Dict[str, Any], 
                             network_data: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Analyze detected anomaly for threat indicators"""
        try:
            idx = anomaly['index']
            conn = network_data[idx]
            
            # Check against threat intelligence
            dst_ip = conn.get('dst_ip')
            if dst_ip and await self._check_ip_reputation(dst_ip):
                return {
                    'type': 'malicious_communication',
                    'severity': 'high',
                    'description': f"Communication with known malicious IP: {dst_ip}",
                    'indicators': [dst_ip],
                    'confidence': anomaly['confidence'],
                    'timestamp': conn.get('timestamp'),
                    'details': conn
                }
                
            # Check for unusual port usage
            dst_port = conn.get('dst_port')
            if dst_port and self._is_unusual_port(dst_port):
                return {
                    'type': 'unusual_port_activity',
                    'severity': 'medium',
                    'description': f"Unusual port activity detected: {dst_port}",
                    'indicators': [f"port:{dst_port}"],
                    'confidence': anomaly['confidence'] * 0.7,
                    'timestamp': conn.get('timestamp'),
                    'details': conn
                }
                
            return None
            
        except Exception as e:
            self.logger.error(f"Error analyzing anomaly: {str(e)}")
            return None
            
    async def _check_ip_reputation(self, ip: str) -> bool:
        """Check IP reputation against threat intelligence"""
        # Check local cache first
        if ip in self.ioc_cache:
            return True
            
        # Check external sources
        if self.ti_sources.get('abuseipdb'):
            try:
                headers = {
                    'Key': self.ti_sources['abuseipdb'],
                    'Accept': 'application/json'
                }
                
                async with self.session.get(
                    f"https://api.abuseipdb.com/api/v2/check",
                    params={'ipAddress': ip, 'maxAgeInDays': 90},
                    headers=headers
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        abuse_confidence = data.get('data', {}).get('abuseConfidencePercentage', 0)
                        return abuse_confidence > 50
                        
            except Exception as e:
                self.logger.error(f"Error checking IP reputation: {str(e)}")
                
        return False
        
    def _is_unusual_port(self, port: int) -> bool:
        """Check if port is unusual/suspicious"""
        # Common legitimate ports
        common_ports = {20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995}
        
        # High ports often used by malware
        if port > 49152:
            return True
            
        # Not in common ports and not in ephemeral range
        if port not in common_ports and port < 32768:
            return True
            
        return False
        
    async def _search_ioc_in_logs(self, ioc: str) -> List[Dict[str, Any]]:
        """Search for IOC in system logs"""
        findings = []
        
        # This would integrate with log management systems
        # Mock implementation
        if self._is_ip_address(ioc):
            # Search for IP in logs
            finding = {
                'type': 'ioc_match',
                'severity': 'high',
                'description': f"Known malicious IP found in logs: {ioc}",
                'indicators': [ioc],
                'confidence': 0.9,
                'timestamp': datetime.utcnow(),
                'source': 'system_logs'
            }
            findings.append(finding)
            
        return findings
        
    def _is_ip_address(self, value: str) -> bool:
        """Check if value is an IP address"""
        import ipaddress
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False
            
    async def _load_threat_intelligence(self):
        """Load threat intelligence from various sources"""
        try:
            # Load from MISP
            if self.ti_sources.get('misp'):
                await self._load_misp_indicators()
                
            # Load from OTX
            if self.ti_sources.get('otx'):
                await self._load_otx_indicators()
                
            self.logger.info(f"Loaded {len(self.ioc_cache)} threat indicators")
            
        except Exception as e:
            self.logger.error(f"Error loading threat intelligence: {str(e)}")
            
    async def _load_misp_indicators(self):
        """Load indicators from MISP"""
        # Implementation would connect to MISP API
        pass
        
    async def _load_otx_indicators(self):
        """Load indicators from AlienVault OTX"""
        # Implementation would connect to OTX API
        pass
        
    def _calculate_hunt_confidence(self, hunt: ThreatHunt) -> float:
        """Calculate overall confidence score for hunt"""
        if not hunt.findings:
            return 0.0
            
        # Weight findings by severity and confidence
        total_score = 0.0
        total_weight = 0.0
        
        severity_weights = {
            'critical': 1.0,
            'high': 0.8,
            'medium': 0.6,
            'low': 0.4,
            'info': 0.2
        }
        
        for finding in hunt.findings:
            severity = finding.get('severity', 'medium')
            confidence = finding.get('confidence', 0.5)
            weight = severity_weights.get(severity, 0.5)
            
            total_score += confidence * weight
            total_weight += weight
            
        return total_score / total_weight if total_weight > 0 else 0.0
        
    def _extract_iocs_from_anomaly(self, anomaly: Dict[str, Any]) -> List[ThreatIndicator]:
        """Extract IOCs from detected anomaly"""
        # Implementation would extract relevant IOCs
        return []
        
    async def get_hunt_status(self, hunt_id: str) -> Optional[Dict[str, Any]]:
        """Get status of active hunt"""
        hunt = self.active_hunts.get(hunt_id)
        if not hunt:
            return None
            
        return {
            'hunt_id': hunt.hunt_id,
            'name': hunt.name,
            'status': hunt.status,
            'start_time': hunt.start_time.isoformat(),
            'findings_count': len(hunt.findings),
            'iocs_discovered': len(hunt.iocs_discovered),
            'confidence_score': hunt.confidence_score,
            'findings': hunt.findings[-5:]  # Last 5 findings
        }
        
    async def stop_hunt(self, hunt_id: str) -> bool:
        """Stop active hunt"""
        hunt = self.active_hunts.get(hunt_id)
        if not hunt:
            return False
            
        hunt.status = 'completed'
        hunt.end_time = datetime.utcnow()
        
        self.logger.info(f"Stopped hunt: {hunt_id}")
        return True

# Additional placeholder methods for comprehensive threat hunting
    async def _detect_auth_anomalies(self) -> List[Dict[str, Any]]:
        """Detect authentication anomalies"""
        return []
        
    async def _detect_lateral_network_patterns(self) -> List[Dict[str, Any]]:
        """Detect lateral movement network patterns"""
        return []
        
    async def _detect_privilege_escalation(self) -> List[Dict[str, Any]]:
        """Detect privilege escalation indicators"""
        return []
        
    async def _detect_remote_access_tools(self) -> List[Dict[str, Any]]:
        """Detect remote access tools"""
        return []
        
    async def _detect_data_transfer_anomalies(self) -> List[Dict[str, Any]]:
        """Detect unusual data transfer patterns"""
        return []
        
    async def _detect_dns_tunneling(self) -> List[Dict[str, Any]]:
        """Detect DNS tunneling"""
        return []
        
    async def _detect_steganography(self) -> List[Dict[str, Any]]:
        """Detect steganography indicators"""
        return []
        
    async def _detect_suspicious_cloud_activity(self) -> List[Dict[str, Any]]:
        """Detect suspicious cloud storage activity"""
        return []
        
    async def _search_ioc_in_network(self, ioc: str) -> List[Dict[str, Any]]:
        """Search for IOC in network traffic"""
        return []
        
    async def _search_ioc_in_dns(self, ioc: str) -> List[Dict[str, Any]]:
        """Search for IOC in DNS queries"""
        return []
        
    async def _hunt_persistence(self, hunt: ThreatHunt, config: Dict[str, Any]):
        """Hunt for persistence mechanisms"""
        pass
        
    async def _hunt_generic_threats(self, hunt: ThreatHunt, config: Dict[str, Any]):
        """Generic threat hunting"""
        pass

# Example usage
async def main():
    """Example usage of threat hunting agent"""
    config = {
        'virustotal_api_key': 'your-vt-key',
        'abuseipdb_api_key': 'your-abuseipdb-key',
        'otx_api_key': 'your-otx-key',
        'misp_url': 'https://misp.company.com'
    }
    
    agent = ThreatHuntingAgent(config)
    await agent.initialize()
    
    try:
        # Start behavioral analysis hunt
        hunt_config = {
            'name': 'Behavioral Anomaly Detection',
            'type': 'behavioral_analysis',
            'description': 'Hunt for behavioral anomalies in network traffic',
            'hypothesis': 'Unusual network patterns may indicate compromise'
        }
        
        hunt_id = await agent.start_hunt(hunt_config)
        print(f"Started hunt: {hunt_id}")
        
        # Check status
        await asyncio.sleep(5)
        status = await agent.get_hunt_status(hunt_id)
        print(f"Hunt status: {status}")
        
    finally:
        await agent.close()

if __name__ == "__main__":
    asyncio.run(main())