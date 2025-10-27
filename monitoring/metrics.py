# monitoring/metrics.py
"""
Prometheus metrics collection for HexStrike AI monitoring
"""
import time
import logging
from typing import Dict, Any, List, Optional
from prometheus_client import Counter, Histogram, Gauge, Info, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry, REGISTRY
from flask import Response
import psutil
import threading


logger = logging.getLogger(__name__)


class MetricsCollector:
    """Prometheus metrics collector for HexStrike AI"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MetricsCollector, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            # Initialize metrics
            self._init_system_metrics()
            self._init_application_metrics()
            self._init_security_metrics()
            self._init_grafana_metrics()
            
            # Start background metric collection
            self._start_background_collection()
            
            MetricsCollector._initialized = True
    
    def _init_system_metrics(self):
        """Initialize system-level metrics"""
        # System information
        self.system_info = Info('hexstrike_system_info', 'System information')
        self.system_info.info({
            'version': '1.0.0',
            'python_version': '3.9+',
            'platform': 'linux'
        })
        
        # System resource metrics
        self.cpu_usage = Gauge('hexstrike_cpu_usage_percent', 'CPU usage percentage')
        self.memory_usage = Gauge('hexstrike_memory_usage_bytes', 'Memory usage in bytes')
        self.memory_total = Gauge('hexstrike_memory_total_bytes', 'Total memory in bytes')
        self.disk_usage = Gauge('hexstrike_disk_usage_bytes', 'Disk usage in bytes', ['device'])
        self.disk_total = Gauge('hexstrike_disk_total_bytes', 'Total disk space in bytes', ['device'])
        
        # Network metrics
        self.network_bytes_sent = Counter('hexstrike_network_bytes_sent_total', 'Network bytes sent')
        self.network_bytes_recv = Counter('hexstrike_network_bytes_recv_total', 'Network bytes received')
    
    def _init_application_metrics(self):
        """Initialize application-level metrics"""
        # HTTP request metrics
        self.http_requests_total = Counter(
            'hexstrike_http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status']
        )
        
        self.http_request_duration = Histogram(
            'hexstrike_http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint']
        )
        
        # Active connections and sessions
        self.active_connections = Gauge('hexstrike_active_connections', 'Number of active connections')
        self.active_sessions = Gauge('hexstrike_active_sessions', 'Number of active user sessions')
        
        # Application health
        self.app_health = Gauge('hexstrike_app_health', 'Application health status (1=healthy, 0=unhealthy)')
        self.app_uptime = Gauge('hexstrike_app_uptime_seconds', 'Application uptime in seconds')
        
        # Database metrics
        self.db_connections = Gauge('hexstrike_db_connections', 'Number of database connections')
        self.db_query_duration = Histogram(
            'hexstrike_db_query_duration_seconds',
            'Database query duration in seconds',
            ['operation']
        )
    
    def _init_security_metrics(self):
        """Initialize security-specific metrics"""
        # Scan metrics
        self.scan_requests_total = Counter(
            'hexstrike_scan_requests_total',
            'Total scan requests',
            ['tool', 'status', 'target_type']
        )
        
        self.scan_duration = Histogram(
            'hexstrike_scan_duration_seconds',
            'Scan duration in seconds',
            ['tool', 'target_type']
        )
        
        self.active_scans = Gauge('hexstrike_active_scans', 'Number of active scans')
        
        # Tool metrics
        self.tool_executions_total = Counter(
            'hexstrike_tool_executions_total',
            'Total tool executions',
            ['tool', 'status']
        )
        
        self.tool_execution_duration = Histogram(
            'hexstrike_tool_execution_duration_seconds',
            'Tool execution duration in seconds',
            ['tool']
        )
        
        self.tool_timeouts_total = Counter(
            'hexstrike_tool_timeouts_total',
            'Total tool timeouts',
            ['tool']
        )
        
        self.tool_success_rate = Gauge(
            'hexstrike_tool_success_rate',
            'Tool success rate (0-1)',
            ['tool']
        )
        
        # Vulnerability metrics
        self.vulnerabilities_found_total = Counter(
            'hexstrike_vulnerabilities_found_total',
            'Total vulnerabilities found',
            ['severity', 'tool', 'type']
        )
        
        self.vulnerability_score = Histogram(
            'hexstrike_vulnerability_score',
            'Vulnerability CVSS scores',
            ['severity', 'tool']
        )
        
        # Authentication metrics
        self.auth_requests_total = Counter(
            'hexstrike_auth_requests_total',
            'Total authentication requests',
            ['status', 'method']
        )
        
        self.auth_failures_total = Counter(
            'hexstrike_auth_failures_total',
            'Total authentication failures',
            ['reason']
        )
        
        # Security events
        self.security_events_total = Counter(
            'hexstrike_security_events_total',
            'Total security events',
            ['event_type', 'severity']
        )
        
        self.suspicious_requests_total = Counter(
            'hexstrike_suspicious_requests_total',
            'Total suspicious requests',
            ['type', 'source']
        )
    
    def _init_grafana_metrics(self):
        """Initialize Grafana-specific metrics"""
        # Grafana health
        self.grafana_health = Gauge('hexstrike_grafana_health', 'Grafana health status (1=healthy, 0=unhealthy)')
        
        # Dashboard metrics
        self.grafana_dashboards_total = Gauge('hexstrike_grafana_dashboards_total', 'Total number of Grafana dashboards')
        self.grafana_users_total = Gauge('hexstrike_grafana_users_total', 'Total number of Grafana users')
        
        # Data source metrics
        self.grafana_datasources_total = Gauge('hexstrike_grafana_datasources_total', 'Total number of Grafana data sources')
        self.grafana_datasource_health = Gauge(
            'hexstrike_grafana_datasource_health',
            'Grafana data source health (1=healthy, 0=unhealthy)',
            ['datasource']
        )
        
        # Alert metrics
        self.grafana_alerts_total = Gauge('hexstrike_grafana_alerts_total', 'Total number of Grafana alerts')
        self.grafana_alerts_firing = Gauge('hexstrike_grafana_alerts_firing', 'Number of firing Grafana alerts')
        
        # Webhook metrics
        self.webhook_deliveries_total = Counter(
            'hexstrike_webhook_deliveries_total',
            'Total webhook deliveries',
            ['endpoint', 'status']
        )
        
        self.webhook_delivery_duration = Histogram(
            'hexstrike_webhook_delivery_duration_seconds',
            'Webhook delivery duration in seconds',
            ['endpoint']
        )
        
        self.webhook_delivery_failures_total = Counter(
            'hexstrike_webhook_delivery_failures_total',
            'Total webhook delivery failures',
            ['endpoint', 'error_type']
        )
        
        self.webhook_queue_size = Gauge('hexstrike_webhook_queue_size', 'Webhook delivery queue size')
    
    def _start_background_collection(self):
        """Start background thread for collecting system metrics"""
        def collect_system_metrics():
            while True:
                try:
                    # CPU usage
                    cpu_percent = psutil.cpu_percent(interval=1)
                    self.cpu_usage.set(cpu_percent)
                    
                    # Memory usage
                    memory = psutil.virtual_memory()
                    self.memory_usage.set(memory.used)
                    self.memory_total.set(memory.total)
                    
                    # Disk usage
                    for partition in psutil.disk_partitions():
                        try:
                            disk_usage = psutil.disk_usage(partition.mountpoint)
                            device = partition.device.replace('/', '_').replace('\\', '_')
                            self.disk_usage.labels(device=device).set(disk_usage.used)
                            self.disk_total.labels(device=device).set(disk_usage.total)
                        except (PermissionError, FileNotFoundError):
                            continue
                    
                    # Network I/O
                    net_io = psutil.net_io_counters()
                    if net_io:
                        self.network_bytes_sent._value._value = net_io.bytes_sent
                        self.network_bytes_recv._value._value = net_io.bytes_recv
                    
                except Exception as e:
                    logger.error(f"Error collecting system metrics: {str(e)}")
                
                time.sleep(30)  # Collect every 30 seconds
        
        thread = threading.Thread(target=collect_system_metrics, daemon=True)
        thread.start()
    
    # HTTP request tracking methods
    def record_http_request(self, method: str, endpoint: str, status: str, duration: float):
        """Record HTTP request metrics"""
        self.http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
        self.http_request_duration.labels(method=method, endpoint=endpoint).observe(duration)
    
    # Scan tracking methods
    def record_scan_request(self, tool: str, status: str, target_type: str = "unknown"):
        """Record scan request metrics"""
        self.scan_requests_total.labels(tool=tool, status=status, target_type=target_type).inc()
    
    def record_scan_duration(self, tool: str, duration: float, target_type: str = "unknown"):
        """Record scan duration metrics"""
        self.scan_duration.labels(tool=tool, target_type=target_type).observe(duration)
    
    def set_active_scans(self, count: int):
        """Set number of active scans"""
        self.active_scans.set(count)
    
    # Tool tracking methods
    def record_tool_execution(self, tool: str, status: str, duration: float):
        """Record tool execution metrics"""
        self.tool_executions_total.labels(tool=tool, status=status).inc()
        self.tool_execution_duration.labels(tool=tool).observe(duration)
    
    def record_tool_timeout(self, tool: str):
        """Record tool timeout"""
        self.tool_timeouts_total.labels(tool=tool).inc()
    
    def update_tool_success_rate(self, tool: str, success_rate: float):
        """Update tool success rate"""
        self.tool_success_rate.labels(tool=tool).set(success_rate)
    
    # Vulnerability tracking methods
    def record_vulnerability(self, severity: str, tool: str, vuln_type: str, cvss_score: float = None):
        """Record vulnerability discovery"""
        self.vulnerabilities_found_total.labels(severity=severity, tool=tool, type=vuln_type).inc()
        if cvss_score is not None:
            self.vulnerability_score.labels(severity=severity, tool=tool).observe(cvss_score)
    
    # Authentication tracking methods
    def record_auth_request(self, status: str, method: str = "oauth"):
        """Record authentication request"""
        self.auth_requests_total.labels(status=status, method=method).inc()
    
    def record_auth_failure(self, reason: str):
        """Record authentication failure"""
        self.auth_failures_total.labels(reason=reason).inc()
    
    # Security event tracking methods
    def record_security_event(self, event_type: str, severity: str):
        """Record security event"""
        self.security_events_total.labels(event_type=event_type, severity=severity).inc()
    
    def record_suspicious_request(self, request_type: str, source: str):
        """Record suspicious request"""
        self.suspicious_requests_total.labels(type=request_type, source=source).inc()
    
    # Grafana tracking methods
    def update_grafana_health(self, is_healthy: bool):
        """Update Grafana health status"""
        self.grafana_health.set(1 if is_healthy else 0)
    
    def update_grafana_stats(self, dashboards: int, users: int, datasources: int, alerts: int, firing_alerts: int):
        """Update Grafana statistics"""
        self.grafana_dashboards_total.set(dashboards)
        self.grafana_users_total.set(users)
        self.grafana_datasources_total.set(datasources)
        self.grafana_alerts_total.set(alerts)
        self.grafana_alerts_firing.set(firing_alerts)
    
    def update_datasource_health(self, datasource: str, is_healthy: bool):
        """Update data source health"""
        self.grafana_datasource_health.labels(datasource=datasource).set(1 if is_healthy else 0)
    
    # Webhook tracking methods
    def record_webhook_delivery(self, endpoint: str, status: str, duration: float):
        """Record webhook delivery"""
        self.webhook_deliveries_total.labels(endpoint=endpoint, status=status).inc()
        self.webhook_delivery_duration.labels(endpoint=endpoint).observe(duration)
    
    def record_webhook_failure(self, endpoint: str, error_type: str):
        """Record webhook delivery failure"""
        self.webhook_delivery_failures_total.labels(endpoint=endpoint, error_type=error_type).inc()
    
    def update_webhook_queue_size(self, size: int):
        """Update webhook queue size"""
        self.webhook_queue_size.set(size)
    
    # Application health methods
    def update_app_health(self, is_healthy: bool):
        """Update application health status"""
        self.app_health.set(1 if is_healthy else 0)
    
    def update_app_uptime(self, uptime_seconds: float):
        """Update application uptime"""
        self.app_uptime.set(uptime_seconds)
    
    def update_active_connections(self, count: int):
        """Update active connections count"""
        self.active_connections.set(count)
    
    def update_active_sessions(self, count: int):
        """Update active sessions count"""
        self.active_sessions.set(count)
    
    # Database methods
    def update_db_connections(self, count: int):
        """Update database connections count"""
        self.db_connections.set(count)
    
    def record_db_query(self, operation: str, duration: float):
        """Record database query"""
        self.db_query_duration.labels(operation=operation).observe(duration)
    
    def get_metrics(self) -> str:
        """Get all metrics in Prometheus format"""
        return generate_latest().decode('utf-8')
    
    def get_metrics_response(self) -> Response:
        """Get Flask response with metrics"""
        return Response(self.get_metrics(), mimetype=CONTENT_TYPE_LATEST)
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of key metrics"""
        # Helper function to safely get counter values
        def get_counter_total(counter):
            try:
                total = 0
                for family in counter.collect():
                    for sample in family.samples:
                        total += sample.value
                return total
            except:
                return 0
        
        return {
            "system": {
                "cpu_usage": self.cpu_usage._value._value,
                "memory_usage_mb": self.memory_usage._value._value / (1024 * 1024),
                "active_scans": self.active_scans._value._value,
                "active_connections": self.active_connections._value._value
            },
            "security": {
                "total_scans": get_counter_total(self.scan_requests_total),
                "total_vulnerabilities": get_counter_total(self.vulnerabilities_found_total),
                "auth_failures": get_counter_total(self.auth_failures_total)
            },
            "grafana": {
                "health": self.grafana_health._value._value,
                "dashboards": self.grafana_dashboards_total._value._value,
                "users": self.grafana_users_total._value._value,
                "alerts_firing": self.grafana_alerts_firing._value._value
            }
        }


# Global metrics collector instance
metrics_collector = MetricsCollector()