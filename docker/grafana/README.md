# HexStrike AI Grafana Monitoring Setup

This directory contains the Grafana configuration and dashboards for HexStrike AI system monitoring.

## Overview

The monitoring system provides six main dashboards:

### System Monitoring Dashboards
1. **System Overview** - High-level system health and activity metrics
2. **Performance Monitoring** - API response times and performance metrics  
3. **Resource Utilization** - CPU, memory, disk, and network usage

### Security Monitoring Dashboards
4. **Scan Activity** - Real-time scan progress and activity monitoring
5. **Vulnerability Trends** - Vulnerability discovery trends with severity breakdown
6. **Tool Performance** - Security tool success rates and execution times

## Directory Structure

```
docker/grafana/
├── README.md                           # This file
├── Dockerfile                          # Grafana container build
├── grafana.ini                         # Grafana configuration
└── provisioning/                       # Auto-provisioning configs
    ├── datasources/
    │   └── prometheus.yml              # Prometheus datasource config
    └── dashboards/
        ├── dashboard.yml               # Dashboard provider config
        ├── system/                     # System monitoring dashboards
        │   ├── overview-dashboard.json
        │   ├── performance-dashboard.json
        │   └── resource-utilization-dashboard.json
        └── security/                   # Security monitoring dashboards
            ├── scan-activity-dashboard.json
            ├── vulnerability-trends-dashboard.json
            └── tool-performance-dashboard.json
```

## Quick Start

### 1. Start Grafana with Docker Compose

```bash
# Start Grafana and Prometheus
docker-compose -f docker-compose.grafana.yml up -d

# Check service status
docker-compose -f docker-compose.grafana.yml ps
```

### 2. Deploy Dashboards

Using Python script:
```bash
# Deploy all system monitoring dashboards
python scripts/deploy-dashboards.py deploy

# Deploy security-specific dashboards
python scripts/deploy-security-dashboards.py deploy

# Validate deployment
python scripts/deploy-dashboards.py validate
python scripts/deploy-security-dashboards.py validate

# Show dashboard URLs
python scripts/deploy-dashboards.py urls
python scripts/deploy-security-dashboards.py urls
```

Using PowerShell (Windows):
```powershell
# Deploy all dashboards
.\scripts\deploy-dashboards.ps1 deploy

# Deploy security dashboards
.\scripts\deploy-security-dashboards.ps1 deploy

# Check Grafana health
.\scripts\deploy-dashboards.ps1 health
.\scripts\deploy-security-dashboards.ps1 health
```

### 3. Access Dashboards

Default Grafana access:
- URL: http://localhost:3000
- Username: admin
- Password: admin (change on first login)

Dashboard URLs:
- System Overview: http://localhost:3000/d/hexstrike-overview
- Performance Monitoring: http://localhost:3000/d/hexstrike-performance  
- Resource Utilization: http://localhost:3000/d/hexstrike-resources
- Scan Activity: http://localhost:3000/d/hexstrike-scan-activity
- Vulnerability Trends: http://localhost:3000/d/hexstrike-vulnerability-trends
- Tool Performance: http://localhost:3000/d/hexstrike-tool-performance

## Dashboard Details

### Security Monitoring Dashboards

#### Scan Activity Dashboard

**Purpose**: Provides real-time monitoring of security scan activities and progress

**Key Metrics**:
- Scan request rate (per 5 minutes)
- Active scans gauge
- Scan requests by tool (pie chart)
- Scan requests by target type (pie chart)
- Scan duration percentiles (95th and 50th)
- Scan status distribution (success, failed, timeout)

**Use Cases**:
- Real-time scan monitoring
- Identifying scan bottlenecks
- Tracking scan performance
- Monitoring scan queue status

#### Vulnerability Trends Dashboard

**Purpose**: Tracks vulnerability discovery trends with detailed severity breakdown

**Key Metrics**:
- Total vulnerabilities found (24h)
- Critical vulnerabilities count (24h)
- High vulnerabilities count (24h)
- High-risk vulnerability ratio
- Vulnerability distribution by severity (pie chart)
- Vulnerabilities by detection tool (pie chart)
- Vulnerability discovery rate by severity (time series)
- CVSS score distribution (percentiles)
- Vulnerabilities by type (pie chart)

**Use Cases**:
- Security posture assessment
- Vulnerability trend analysis
- Risk prioritization
- Tool effectiveness evaluation
- Compliance reporting

#### Tool Performance Dashboard

**Purpose**: Monitors security tool performance, success rates, and execution metrics

**Key Metrics**:
- Tool success rates (bar gauge)
- Tool execution time percentiles (95th and 50th)
- Tool execution rate by status
- Tool execution status distribution (success, failed, timeout)
- Tool usage distribution
- Tool timeout rates
- Top 10 most used tools (24h)
- Top 10 vulnerability detection tools (24h)

**Use Cases**:
- Tool performance optimization
- Identifying unreliable tools
- Resource allocation planning
- Tool effectiveness comparison
- Performance troubleshooting

### System Monitoring Dashboards

#### System Overview Dashboard

**Purpose**: Provides a high-level view of system health and activity

**Key Metrics**:
- CPU usage percentage
- Memory usage gauge
- Active scans, connections, and sessions
- Service health status (Application, Grafana)
- HTTP request rate
- Scan request rate

**Use Cases**:
- Quick system health check
- Monitoring overall system activity
- Identifying service outages

### Performance Monitoring Dashboard

**Purpose**: Monitors API performance and response times

**Key Metrics**:
- API response time percentiles (50th, 95th, 99th)
- Average response time by endpoint
- HTTP request rate by status code (2xx, 4xx, 5xx)
- API success rate gauge
- Database query performance
- Database connection count

**Use Cases**:
- Identifying performance bottlenecks
- Monitoring API health
- Database performance analysis
- SLA monitoring

### Resource Utilization Dashboard

**Purpose**: Tracks system resource consumption

**Key Metrics**:
- CPU utilization over time
- Memory usage (used, total, available)
- Memory and CPU usage gauges
- Disk usage by device
- Network I/O (bytes sent/received)
- Disk I/O operations

**Use Cases**:
- Capacity planning
- Resource optimization
- Performance troubleshooting
- Infrastructure monitoring

## Configuration

### Environment Variables

Configure Grafana using environment variables:

```bash
# Basic configuration
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=your_secure_password
GRAFANA_SECRET_KEY=your_secret_key
GRAFANA_DOMAIN=your-domain.com

# Auth0 integration (optional)
GRAFANA_AUTH0_ENABLED=true
GRAFANA_AUTH0_CLIENT_ID=your_auth0_client_id
GRAFANA_AUTH0_CLIENT_SECRET=your_auth0_client_secret
GRAFANA_AUTH0_DOMAIN=your-auth0-domain.auth0.com

# Prometheus configuration
PROMETHEUS_URL=http://prometheus:9090
```

### Custom Dashboards

To add custom dashboards:

1. Create dashboard JSON file in appropriate folder:
   - System dashboards: `provisioning/dashboards/system/`
   - Security dashboards: `provisioning/dashboards/scans/`
   - Tool dashboards: `provisioning/dashboards/tools/`
   - User dashboards: `provisioning/dashboards/users/`

2. Update `monitoring/dashboard_manager.py` to include new dashboard

3. Deploy using the dashboard manager scripts

### Data Sources

The system automatically configures:
- **Prometheus**: Primary metrics data source
- **Prometheus-LongTerm**: For historical data (if using Thanos)

## Troubleshooting

### Common Issues

**Dashboard not loading**:
```bash
# Check Grafana logs
docker logs hexstrike-grafana

# Verify Prometheus connectivity
curl http://localhost:9090/-/healthy
```

**Missing metrics**:
```bash
# Check if HexStrike AI is exposing metrics
curl http://localhost:8000/metrics

# Verify Prometheus is scraping
curl http://localhost:9090/api/v1/targets
```

**Authentication issues**:
```bash
# Reset admin password
docker exec -it hexstrike-grafana grafana-cli admin reset-admin-password newpassword
```

### Health Checks

Use the built-in health checker:

```python
from monitoring.health_checks import HealthChecker

checker = HealthChecker()
health = checker.get_overall_health()
print(f"System health: {health['overall_status']}")
```

### Dashboard Validation

Validate dashboard deployment:

```python
from monitoring.dashboard_manager import DashboardManager

manager = DashboardManager()
validation = manager.validate_dashboards()

if validation["valid"]:
    print("All dashboards are properly deployed")
else:
    print(f"Issues found: {validation['summary']}")
```

## Metrics Reference

### Application Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `hexstrike_cpu_usage_percent` | Gauge | CPU usage percentage |
| `hexstrike_memory_usage_bytes` | Gauge | Memory usage in bytes |
| `hexstrike_memory_total_bytes` | Gauge | Total memory in bytes |
| `hexstrike_active_scans` | Gauge | Number of active scans |
| `hexstrike_active_connections` | Gauge | Number of active connections |
| `hexstrike_active_sessions` | Gauge | Number of active user sessions |
| `hexstrike_app_health` | Gauge | Application health (1=healthy, 0=unhealthy) |
| `hexstrike_grafana_health` | Gauge | Grafana health (1=healthy, 0=unhealthy) |

### HTTP Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `hexstrike_http_requests_total` | Counter | method, endpoint, status | Total HTTP requests |
| `hexstrike_http_request_duration_seconds` | Histogram | method, endpoint | HTTP request duration |

### Security Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `hexstrike_scan_requests_total` | Counter | tool, status, target_type | Total scan requests |
| `hexstrike_scan_duration_seconds` | Histogram | tool, target_type | Scan duration |
| `hexstrike_vulnerabilities_found_total` | Counter | severity, tool, type | Total vulnerabilities found |

### Database Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `hexstrike_db_connections` | Gauge | - | Number of database connections |
| `hexstrike_db_query_duration_seconds` | Histogram | operation | Database query duration |

## Security Considerations

1. **Change default credentials** immediately after setup
2. **Enable HTTPS** in production environments
3. **Configure proper authentication** (Auth0, LDAP, etc.)
4. **Restrict network access** to Grafana port (3000)
5. **Regular security updates** for Grafana and dependencies
6. **Monitor access logs** for suspicious activity

## Performance Optimization

1. **Data retention**: Configure appropriate retention policies
2. **Query optimization**: Use efficient Prometheus queries
3. **Dashboard refresh rates**: Balance between real-time data and performance
4. **Resource limits**: Set appropriate CPU/memory limits for containers
5. **Caching**: Enable Grafana caching for better performance

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review Grafana logs: `docker logs hexstrike-grafana`
3. Validate metrics exposure: `curl http://localhost:8000/metrics`
4. Test Prometheus connectivity: `curl http://localhost:9090/-/healthy`

## References

- [Grafana Documentation](https://grafana.com/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [HexStrike AI Monitoring Guide](../../monitoring/README.md)