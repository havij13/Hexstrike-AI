"""
Scan Model

This module contains the Scan data model and related functionality.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ScanStatus(Enum):
    """Scan status enumeration"""
    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class ScanType(Enum):
    """Scan type enumeration"""
    RECONNAISSANCE = "reconnaissance"
    VULNERABILITY_SCAN = "vulnerability_scan"
    NETWORK_DISCOVERY = "network_discovery"
    WEB_APPLICATION = "web_application"
    API_TESTING = "api_testing"
    BUG_BOUNTY = "bug_bounty"
    CTF = "ctf"
    CUSTOM = "custom"


@dataclass
class ScanResult:
    """Scan result data"""
    vulnerabilities: List[Dict[str, Any]] = field(default_factory=list)
    open_ports: List[int] = field(default_factory=list)
    services: Dict[str, Any] = field(default_factory=dict)
    technologies: List[str] = field(default_factory=list)
    endpoints: List[str] = field(default_factory=list)
    raw_output: Dict[str, str] = field(default_factory=dict)
    statistics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Scan:
    """Scan data model"""
    id: str
    target: str
    scan_type: ScanType
    status: ScanStatus
    user_id: str
    tenant_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    tools_used: List[str] = field(default_factory=list)
    results: Optional[ScanResult] = None
    progress: int = 0
    error_message: Optional[str] = None
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert scan to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'target': self.target,
            'scan_type': self.scan_type.value if isinstance(self.scan_type, ScanType) else self.scan_type,
            'status': self.status.value if isinstance(self.status, ScanStatus) else self.status,
            'user_id': self.user_id,
            'tenant_id': self.tenant_id,
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters,
            'tools_used': self.tools_used,
            'results': self._serialize_results(),
            'progress': self.progress,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'tags': self.tags,
            'metadata': self.metadata
        }

    def _serialize_results(self) -> Optional[Dict[str, Any]]:
        """Serialize scan results"""
        if not self.results:
            return None
        
        return {
            'vulnerabilities': self.results.vulnerabilities,
            'open_ports': self.results.open_ports,
            'services': self.results.services,
            'technologies': self.results.technologies,
            'endpoints': self.results.endpoints,
            'raw_output': self.results.raw_output,
            'statistics': self.results.statistics
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Scan':
        """Create Scan instance from dictionary"""
        # Parse results if present
        results = None
        if data.get('results'):
            results_data = data['results']
            results = ScanResult(
                vulnerabilities=results_data.get('vulnerabilities', []),
                open_ports=results_data.get('open_ports', []),
                services=results_data.get('services', {}),
                technologies=results_data.get('technologies', []),
                endpoints=results_data.get('endpoints', []),
                raw_output=results_data.get('raw_output', {}),
                statistics=results_data.get('statistics', {})
            )

        return cls(
            id=data['id'],
            target=data['target'],
            scan_type=ScanType(data['scan_type']) if isinstance(data['scan_type'], str) else data['scan_type'],
            status=ScanStatus(data['status']) if isinstance(data['status'], str) else data['status'],
            user_id=data['user_id'],
            tenant_id=data['tenant_id'],
            name=data.get('name'),
            description=data.get('description'),
            parameters=data.get('parameters', {}),
            tools_used=data.get('tools_used', []),
            results=results,
            progress=data.get('progress', 0),
            error_message=data.get('error_message'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            started_at=datetime.fromisoformat(data['started_at']) if data.get('started_at') else None,
            completed_at=datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            tags=data.get('tags', []),
            metadata=data.get('metadata', {})
        )

    def is_running(self) -> bool:
        """Check if scan is currently running"""
        return self.status in [ScanStatus.QUEUED, ScanStatus.RUNNING]

    def is_completed(self) -> bool:
        """Check if scan is completed (successfully or with failure)"""
        return self.status in [ScanStatus.COMPLETED, ScanStatus.FAILED, ScanStatus.CANCELLED, ScanStatus.TIMEOUT]

    def is_successful(self) -> bool:
        """Check if scan completed successfully"""
        return self.status == ScanStatus.COMPLETED

    def get_duration(self) -> Optional[int]:
        """Get scan duration in seconds"""
        if self.started_at and self.completed_at:
            return int((self.completed_at - self.started_at).total_seconds())
        return None

    def get_vulnerability_count(self) -> int:
        """Get total number of vulnerabilities found"""
        if not self.results:
            return 0
        return len(self.results.vulnerabilities)

    def get_vulnerability_count_by_severity(self) -> Dict[str, int]:
        """Get vulnerability count grouped by severity"""
        if not self.results:
            return {}
        
        severity_counts = {}
        for vuln in self.results.vulnerabilities:
            severity = vuln.get('severity', 'unknown').lower()
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return severity_counts

    def add_tag(self, tag: str):
        """Add tag to scan"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow()

    def remove_tag(self, tag: str):
        """Remove tag from scan"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow()

    def set_metadata(self, key: str, value: Any):
        """Set metadata"""
        self.metadata[key] = value
        self.updated_at = datetime.utcnow()

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata"""
        return self.metadata.get(key, default)

    def update_progress(self, progress: int):
        """Update scan progress"""
        self.progress = max(0, min(100, progress))
        self.updated_at = datetime.utcnow()

    def start(self):
        """Mark scan as started"""
        self.status = ScanStatus.RUNNING
        self.started_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def complete(self, results: ScanResult):
        """Mark scan as completed with results"""
        self.status = ScanStatus.COMPLETED
        self.results = results
        self.progress = 100
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def fail(self, error_message: str):
        """Mark scan as failed"""
        self.status = ScanStatus.FAILED
        self.error_message = error_message
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def cancel(self):
        """Mark scan as cancelled"""
        self.status = ScanStatus.CANCELLED
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()


class ScanSerializer:
    """Scan serializer for API responses"""

    @staticmethod
    def serialize(scan: Scan, include_results: bool = True) -> Dict[str, Any]:
        """Serialize scan for API response"""
        data = scan.to_dict()
        
        if not include_results:
            # Remove detailed results for list views
            if 'results' in data and data['results']:
                data['results'] = {
                    'vulnerability_count': len(data['results'].get('vulnerabilities', [])),
                    'open_ports_count': len(data['results'].get('open_ports', [])),
                    'technologies_count': len(data['results'].get('technologies', []))
                }
        
        return data

    @staticmethod
    def serialize_list(scans: List[Scan], include_results: bool = False) -> List[Dict[str, Any]]:
        """Serialize list of scans for API response"""
        return [ScanSerializer.serialize(scan, include_results) for scan in scans]

    @staticmethod
    def deserialize(data: Dict[str, Any]) -> Scan:
        """Deserialize scan from API request"""
        return Scan.from_dict(data)