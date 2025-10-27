# HexStrike AI Grafana Infrastructure

This directory contains the complete Grafana monitoring infrastructure for HexStrike AI, including dashboards, data sources, and configuration files.

## Quick Start

### 1. Start the Infrastructure

```bash
# Start all monitoring services
docker-compose -f docker-compose.grafana.yml up -d

# Or use the setup script
./scripts/setup-grafana.sh setup
```

### 2. Access Services

- **Grafana Dashboard**: http://localhost:3000 (admin/admin123)
- **Prometheus**: http://localhost:9090
- **Node Exporter**: http://localhost:9100/metrics
- **cAdvisor**: http://localhost:8080

### 3. Verify Setup

```bash
# Check service health
./scripts/setup-grafana.sh status

# Or use Python health checker
python monitoring/health_checks.py
```

## Architecture

### Services

1. **Grafana** (Port 3000)
   - Main dashboard and visualization platform
   - Pre-configured with Prometheus data source
   - Organized dashboards for different aspects of HexStrike AI

2. **Prometheus** (Port 9090)
   - Metrics collection and storage
   - Scrapes metrics from HexStrike AI application
   - Configured with alerting rules

3. **Node Exporter** (Port 9100)
   - System-level metrics (CPU, memory, disk, network)
   - Provides host machine monitoring

4. **cAdvisor** (Port 8080)
   - Container-level metrics
   - Docker container resource usage monitoring

### Dashboard Organization

Dashboards are organized into folders:

- **HexStrike System**: Overall system health and performance
- **Security Scans**: Scan activity, progress, and results
- **Tool Performance**: Individual security tool metrics
- **User Analytics**: User activity and authentication metrics

## Configuration

### Environment Variables

Key environment variables for customization:

```bash
# Grafana Configuration
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin123
GRAFANA_DOMAIN=localhost
GRAFANA_ROOT_URL=http://localhost:3000

# Auth0 Integration (Optional)
GRAFANA_AUTH0_ENABLED=false
GRAFANA_AUTH0_CLIENT_ID=your_client_id
GRAFANA_AUTH0_CLIENT_SECRET=your_client_secret
GRAFANA_AUTH0_DOMAIN=your_domain.auth0.com

# Prometheus
PROMETHEUS_URL=http://prometheus:9090
```

### Auth0 Integration

To enable Auth0 SSO for Grafana:

1. Set up Auth0 application with appropriate callback URLs
2. Configure environment variables:
   ```bash
   GRAFANA_AUTH0_ENABLED=true
   GRAFANA_AUTH0_CLIENT_ID=your_client_id
   GRAFANA_AUTH0_CLIENT_SECRET=your_client_secret
   GRAFANA_AUTH0_DOMAIN=your_domain.auth0.com
   ```
3. Restart Grafana service

### Custom Dashboards

To add custom dashboards:

1. Create JSON dashboard files
2. Place them in the appropriate provisioning directory:
   - System dashboards: `provisioning/dashboards/system/`
   - Scan dashboards: `provisioning/dashboards/scans/`
   - Tool dashboards: `provisioning/dashboards/tools/`
   - User dashboards: `provisioning/dashboards/users/`
3. Restart Grafana to load new dashboards

## Metrics Integration

### HexStrike AI Metrics

The application exposes metrics on `/metrics` endpoint:

```python
from monitoring.metrics import metrics_collector

# Record scan metrics
metrics_collector.record_scan_request('nmap', 'success', 'network')
metrics_collector.record_scan_duration('nmap', 30.5, 'network')

# Record vulnerability findings
metrics_collector.record_vulnerability('high', 'nuclei', 'xss', 7.5)

# Update system health
metrics_collector.update_app_health(True)
```

### Custom Metrics

Add custom metrics by extending the MetricsCollector:

```python
from prometheus_client import Counter

# Define custom metric
custom_metric = Counter('hexstrike_custom_events_total', 'Custom events', ['event_type'])

# Record events
custom_metric.labels(event_type='scan_completed').inc()
```

## Alerting

### Prometheus Alerts

Alert rules are defined in `prometheus/rules/hexstrike_alerts.yml`:

- System health alerts (service down, high resource usage)
- Security-specific alerts (scan failures, high error rates)
- Performance alerts (slow response times, timeouts)

### Grafana Notifications

Configure notification channels in Grafana:

1. Go to Alerting > Notification channels
2. Add channels for Slack, email, webhooks, etc.
3. Configure alert rules to use notification channels

## Troubleshooting

### Common Issues

1. **Grafana won't start**
   ```bash
   # Check logs
   docker-compose -f docker-compose.grafana.yml logs grafana
   
   # Verify permissions
   sudo chown -R 472:472 grafana_data/
   ```

2. **Prometheus can't scrape metrics**
   ```bash
   # Check Prometheus targets
   curl http://localhost:9090/api/v1/targets
   
   # Verify HexStrike AI metrics endpoint
   curl http://localhost:5000/metrics
   ```

3. **No data in dashboards**
   ```bash
   # Check data source connection
   curl -u admin:admin123 http://localhost:3000/api/datasources
   
   # Test Prometheus query
   curl "http://localhost:9090/api/v1/query?query=up"
   ```

### Health Checks

Use the built-in health checker:

```bash
# Check all services
python monitoring/health_checks.py

# Check specific service
python -c "
from monitoring.health_checks import HealthChecker
checker = HealthChecker()
health = checker.check_grafana_health()
print(f'Grafana: {health.status.value} - {health.message}')
"
```

### Performance Tuning

For high-load environments:

1. **Increase Prometheus retention**:
   ```yaml
   # In docker-compose.grafana.yml
   command:
     - '--storage.tsdb.retention.time=30d'
   ```

2. **Configure Grafana caching**:
   ```ini
   # In grafana.ini
   [caching]
   enabled = true
   ```

3. **Optimize dashboard queries**:
   - Use appropriate time ranges
   - Limit data points with `$__interval`
   - Use recording rules for complex queries

## Security

### Access Control

- Default admin credentials should be changed in production
- Use Auth0 or LDAP for enterprise authentication
- Configure role-based access control (RBAC)
- Enable HTTPS in production environments

### Network Security

- Use reverse proxy (nginx/traefik) for SSL termination
- Restrict access to monitoring ports
- Configure firewall rules appropriately
- Use VPN for remote access to monitoring infrastructure

## Backup and Recovery

### Grafana Backup

```bash
# Backup Grafana database and configuration
docker exec hexstrike-grafana grafana-cli admin export-dashboard > backup.json

# Backup persistent volumes
docker run --rm -v grafana_data:/data -v $(pwd):/backup alpine tar czf /backup/grafana-backup.tar.gz /data
```

### Prometheus Backup

```bash
# Backup Prometheus data
docker run --rm -v prometheus_data:/data -v $(pwd):/backup alpine tar czf /backup/prometheus-backup.tar.gz /data
```

## Monitoring Best Practices

1. **Dashboard Design**:
   - Use consistent color schemes
   - Group related metrics together
   - Include context and documentation
   - Set appropriate refresh intervals

2. **Alerting Strategy**:
   - Define clear severity levels
   - Avoid alert fatigue with proper thresholds
   - Include runbook links in alert descriptions
   - Test alert delivery regularly

3. **Metrics Collection**:
   - Use appropriate metric types (counter, gauge, histogram)
   - Include relevant labels for filtering
   - Avoid high-cardinality labels
   - Document custom metrics

4. **Performance**:
   - Monitor monitoring system resource usage
   - Set appropriate retention policies
   - Use recording rules for expensive queries
   - Regular cleanup of old data

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Review logs: `docker-compose -f docker-compose.grafana.yml logs`
3. Verify configuration with health checks
4. Consult Grafana and Prometheus documentation
5. Open an issue in the HexStrike AI repository