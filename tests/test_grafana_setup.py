# tests/test_grafana_setup.py
"""
Tests for Grafana infrastructure setup
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import requests
from config.grafana_config import GrafanaConfig, GrafanaAPIConfig
from monitoring.grafana_setup import GrafanaSetup
from monitoring.health_checks import HealthChecker, HealthStatus
from monitoring.metrics import MetricsCollector


class TestGrafanaConfig(unittest.TestCase):
    """Test Grafana configuration"""
    
    def test_grafana_config_defaults(self):
        """Test default Grafana configuration values"""
        config = GrafanaConfig()
        
        self.assertEqual(config.GRAFANA_HOST, 'localhost')
        self.assertEqual(config.GRAFANA_PORT, 3000)
        self.assertEqual(config.GRAFANA_PROTOCOL, 'http')
        self.assertEqual(config.GRAFANA_ADMIN_USER, 'admin')
    
    def test_get_grafana_config(self):
        """Test getting complete Grafana configuration"""
        config = GrafanaConfig.get_grafana_config()
        
        self.assertIn('server', config)
        self.assertIn('database', config)
        self.assertIn('security', config)
        self.assertIn('users', config)
        
        # Check server config
        self.assertEqual(config['server']['http_port'], 3000)
        self.assertEqual(config['server']['protocol'], 'http')
    
    def test_get_prometheus_datasource_config(self):
        """Test Prometheus datasource configuration"""
        config = GrafanaConfig.get_prometheus_datasource_config()
        
        self.assertEqual(config['name'], 'Prometheus')
        self.assertEqual(config['type'], 'prometheus')
        self.assertTrue(config['isDefault'])
        self.assertIn('jsonData', config)
    
    def test_grafana_api_config(self):
        """Test Grafana API configuration"""
        api_config = GrafanaAPIConfig()
        
        self.assertIn('http://localhost:3000', api_config.base_url)
        
        headers = api_config.get_headers()
        self.assertEqual(headers['Content-Type'], 'application/json')
        
        auth = api_config.get_auth()
        self.assertEqual(len(auth), 2)


class TestGrafanaSetup(unittest.TestCase):
    """Test Grafana setup functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.setup = GrafanaSetup()
    
    @patch('requests.Session.get')
    def test_wait_for_grafana_success(self, mock_get):
        """Test waiting for Grafana to be ready - success case"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = self.setup.wait_for_grafana(timeout=5)
        self.assertTrue(result)
    
    @patch('requests.Session.get')
    def test_wait_for_grafana_timeout(self, mock_get):
        """Test waiting for Grafana to be ready - timeout case"""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        result = self.setup.wait_for_grafana(timeout=1)
        self.assertFalse(result)
    
    @patch('requests.Session.get')
    @patch('requests.Session.post')
    def test_setup_prometheus_datasource_new(self, mock_post, mock_get):
        """Test setting up new Prometheus datasource"""
        # Mock datasource doesn't exist
        mock_get.return_value.status_code = 404
        
        # Mock successful creation
        mock_post.return_value.status_code = 200
        
        result = self.setup.setup_prometheus_datasource()
        self.assertTrue(result)
        mock_post.assert_called_once()
    
    @patch('requests.Session.get')
    def test_setup_prometheus_datasource_exists(self, mock_get):
        """Test setting up existing Prometheus datasource"""
        # Mock datasource already exists
        mock_get.return_value.status_code = 200
        
        result = self.setup.setup_prometheus_datasource()
        self.assertTrue(result)
    
    @patch('requests.Session.post')
    def test_create_api_key_success(self, mock_post):
        """Test creating API key successfully"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'key': 'test-api-key-123'}
        mock_post.return_value = mock_response
        
        api_key = self.setup.create_api_key('test-key', 'Admin')
        self.assertEqual(api_key, 'test-api-key-123')
    
    @patch('requests.Session.post')
    def test_create_api_key_failure(self, mock_post):
        """Test creating API key failure"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = 'Bad request'
        mock_post.return_value = mock_response
        
        api_key = self.setup.create_api_key('test-key', 'Admin')
        self.assertIsNone(api_key)


class TestHealthChecker(unittest.TestCase):
    """Test health checking functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.checker = HealthChecker()
    
    @patch('requests.Session.get')
    def test_check_grafana_health_success(self, mock_get):
        """Test successful Grafana health check"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'version': '10.2.0',
            'database': 'ok',
            'commit': 'abc123'
        }
        mock_get.return_value = mock_response
        
        health = self.checker.check_grafana_health()
        
        self.assertEqual(health.service, 'grafana')
        self.assertEqual(health.status, HealthStatus.HEALTHY)
        self.assertEqual(health.details['version'], '10.2.0')
    
    @patch('requests.Session.get')
    def test_check_grafana_health_connection_error(self, mock_get):
        """Test Grafana health check with connection error"""
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        health = self.checker.check_grafana_health()
        
        self.assertEqual(health.service, 'grafana')
        self.assertEqual(health.status, HealthStatus.UNHEALTHY)
        self.assertIn('Cannot connect', health.message)
    
    @patch('requests.Session.get')
    def test_check_prometheus_health_success(self, mock_get):
        """Test successful Prometheus health check"""
        # Mock healthy response
        mock_response = Mock()
        mock_response.status_code = 200
        
        # Mock query response
        mock_query_response = Mock()
        mock_query_response.status_code = 200
        mock_query_response.json.return_value = {
            'data': {
                'result': [
                    {'value': [1234567890, '1']},
                    {'value': [1234567890, '1']}
                ]
            }
        }
        
        mock_get.side_effect = [mock_response, mock_query_response]
        
        health = self.checker.check_prometheus_health()
        
        self.assertEqual(health.service, 'prometheus')
        self.assertEqual(health.status, HealthStatus.HEALTHY)
        self.assertEqual(health.details['targets_up'], 2)
    
    def test_get_overall_health_all_healthy(self):
        """Test overall health when all services are healthy"""
        # Create mock healthy checks
        healthy_checks = [
            Mock(service='grafana', status=HealthStatus.HEALTHY, response_time=0.1),
            Mock(service='prometheus', status=HealthStatus.HEALTHY, response_time=0.2)
        ]
        
        overall = self.checker.get_overall_health(healthy_checks)
        
        self.assertEqual(overall['overall_status'], 'healthy')
        self.assertEqual(overall['healthy_services'], 2)
        self.assertEqual(overall['total_services'], 2)
        self.assertEqual(overall['health_percentage'], 100.0)
    
    def test_get_overall_health_mixed_status(self):
        """Test overall health with mixed service statuses"""
        # Create mock mixed checks
        mixed_checks = [
            Mock(service='grafana', status=HealthStatus.HEALTHY, response_time=0.1),
            Mock(service='prometheus', status=HealthStatus.UNHEALTHY, response_time=5.0)
        ]
        
        overall = self.checker.get_overall_health(mixed_checks)
        
        self.assertEqual(overall['overall_status'], 'unhealthy')
        self.assertEqual(overall['healthy_services'], 1)
        self.assertEqual(overall['total_services'], 2)
        self.assertEqual(overall['health_percentage'], 50.0)


class TestMetricsCollector(unittest.TestCase):
    """Test metrics collection functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Use a separate registry for each test to avoid conflicts
        from prometheus_client import CollectorRegistry
        self.registry = CollectorRegistry()
        
        # Mock the MetricsCollector to use our test registry
        with patch('monitoring.metrics.MetricsCollector._init_system_metrics'), \
             patch('monitoring.metrics.MetricsCollector._init_application_metrics'), \
             patch('monitoring.metrics.MetricsCollector._init_security_metrics'), \
             patch('monitoring.metrics.MetricsCollector._init_grafana_metrics'), \
             patch('monitoring.metrics.MetricsCollector._start_background_collection'):
            self.collector = MetricsCollector()
    
    def test_record_http_request(self):
        """Test recording HTTP request metrics"""
        # This should not raise an exception
        self.collector.record_http_request('GET', '/api/health', '200', 0.1)
        
        # Verify metric was recorded
        metrics_output = self.collector.get_metrics()
        self.assertIn('hexstrike_http_requests_total', metrics_output)
    
    def test_record_scan_metrics(self):
        """Test recording scan metrics"""
        # Record scan request
        self.collector.record_scan_request('nmap', 'success', 'network')
        self.collector.record_scan_duration('nmap', 30.5, 'network')
        self.collector.set_active_scans(5)
        
        # Verify metrics were recorded
        metrics_output = self.collector.get_metrics()
        self.assertIn('hexstrike_scan_requests_total', metrics_output)
        self.assertIn('hexstrike_scan_duration_seconds', metrics_output)
        self.assertIn('hexstrike_active_scans', metrics_output)
    
    def test_record_vulnerability(self):
        """Test recording vulnerability metrics"""
        self.collector.record_vulnerability('high', 'nuclei', 'xss', 7.5)
        
        metrics_output = self.collector.get_metrics()
        self.assertIn('hexstrike_vulnerabilities_found_total', metrics_output)
        self.assertIn('hexstrike_vulnerability_score', metrics_output)
    
    def test_record_auth_metrics(self):
        """Test recording authentication metrics"""
        self.collector.record_auth_request('success', 'oauth')
        self.collector.record_auth_failure('invalid_token')
        
        metrics_output = self.collector.get_metrics()
        self.assertIn('hexstrike_auth_requests_total', metrics_output)
        self.assertIn('hexstrike_auth_failures_total', metrics_output)
    
    def test_update_grafana_metrics(self):
        """Test updating Grafana-specific metrics"""
        self.collector.update_grafana_health(True)
        self.collector.update_grafana_stats(10, 5, 3, 15, 2)
        self.collector.update_datasource_health('prometheus', True)
        
        metrics_output = self.collector.get_metrics()
        self.assertIn('hexstrike_grafana_health', metrics_output)
        self.assertIn('hexstrike_grafana_dashboards_total', metrics_output)
        self.assertIn('hexstrike_grafana_datasource_health', metrics_output)
    
    def test_get_metrics_summary(self):
        """Test getting metrics summary"""
        # Set some test values
        self.collector.set_active_scans(3)
        self.collector.update_grafana_health(True)
        self.collector.update_grafana_stats(5, 2, 1, 8, 1)
        
        summary = self.collector.get_metrics_summary()
        
        self.assertIn('system', summary)
        self.assertIn('security', summary)
        self.assertIn('grafana', summary)
        
        self.assertEqual(summary['system']['active_scans'], 3)
        self.assertEqual(summary['grafana']['health'], 1)
        self.assertEqual(summary['grafana']['dashboards'], 5)


if __name__ == '__main__':
    unittest.main()