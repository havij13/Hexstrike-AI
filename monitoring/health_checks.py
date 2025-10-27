# monitoring/health_checks.py
"""
Health check system for HexStrike AI monitoring infrastructure
"""
import requests
import time
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from config.grafana_config import GrafanaConfig


logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Health status enumeration"""
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Health check result"""
    service: str
    status: HealthStatus
    response_time: float
    message: str
    details: Dict[str, Any] = None
    timestamp: float = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class HealthChecker:
    """Health checker for monitoring infrastructure services"""
    
    def __init__(self):
        self.config = GrafanaConfig()
        self.session = requests.Session()
        self.session.timeout = 10
        
    def check_grafana_health(self) -> HealthCheck:
        """Check Grafana service health"""
        service = "grafana"
        start_time = time.time()
        
        try:
            url = f"{self.config.GRAFANA_PROTOCOL}://{self.config.GRAFANA_HOST}:{self.config.GRAFANA_PORT}/api/health"
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                health_data = response.json()
                return HealthCheck(
                    service=service,
                    status=HealthStatus.HEALTHY,
                    response_time=response_time,
                    message="Grafana is healthy",
                    details={
                        "version": health_data.get("version", "unknown"),
                        "database": health_data.get("database", "unknown"),
                        "commit": health_data.get("commit", "unknown")
                    }
                )
            else:
                return HealthCheck(
                    service=service,
                    status=HealthStatus.UNHEALTHY,
                    response_time=response_time,
                    message=f"Grafana returned HTTP {response.status_code}",
                    details={"status_code": response.status_code}
                )
                
        except requests.exceptions.ConnectionError:
            return HealthCheck(
                service=service,
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                message="Cannot connect to Grafana service"
            )
        except Exception as e:
            return HealthCheck(
                service=service,
                status=HealthStatus.UNKNOWN,
                response_time=time.time() - start_time,
                message=f"Error checking Grafana health: {str(e)}"
            )
    
    def check_prometheus_health(self) -> HealthCheck:
        """Check Prometheus service health"""
        service = "prometheus"
        start_time = time.time()
        
        try:
            url = f"{self.config.PROMETHEUS_URL}/-/healthy"
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                # Also check if Prometheus can query itself
                query_url = f"{self.config.PROMETHEUS_URL}/api/v1/query"
                query_response = self.session.get(query_url, params={"query": "up"})
                
                if query_response.status_code == 200:
                    query_data = query_response.json()
                    targets_up = len([r for r in query_data.get("data", {}).get("result", []) if r.get("value", [None, "0"])[1] == "1"])
                    
                    return HealthCheck(
                        service=service,
                        status=HealthStatus.HEALTHY,
                        response_time=response_time,
                        message="Prometheus is healthy",
                        details={
                            "targets_up": targets_up,
                            "query_response_time": time.time() - start_time - response_time
                        }
                    )
                else:
                    return HealthCheck(
                        service=service,
                        status=HealthStatus.DEGRADED,
                        response_time=response_time,
                        message="Prometheus is up but queries are failing"
                    )
            else:
                return HealthCheck(
                    service=service,
                    status=HealthStatus.UNHEALTHY,
                    response_time=response_time,
                    message=f"Prometheus returned HTTP {response.status_code}"
                )
                
        except requests.exceptions.ConnectionError:
            return HealthCheck(
                service=service,
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                message="Cannot connect to Prometheus service"
            )
        except Exception as e:
            return HealthCheck(
                service=service,
                status=HealthStatus.UNKNOWN,
                response_time=time.time() - start_time,
                message=f"Error checking Prometheus health: {str(e)}"
            )
    
    def check_node_exporter_health(self) -> HealthCheck:
        """Check Node Exporter service health"""
        service = "node-exporter"
        start_time = time.time()
        
        try:
            url = "http://localhost:9100/metrics"
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                # Check if we're getting actual metrics
                metrics_text = response.text
                if "node_" in metrics_text:
                    return HealthCheck(
                        service=service,
                        status=HealthStatus.HEALTHY,
                        response_time=response_time,
                        message="Node Exporter is healthy",
                        details={"metrics_size": len(metrics_text)}
                    )
                else:
                    return HealthCheck(
                        service=service,
                        status=HealthStatus.DEGRADED,
                        response_time=response_time,
                        message="Node Exporter is up but not returning expected metrics"
                    )
            else:
                return HealthCheck(
                    service=service,
                    status=HealthStatus.UNHEALTHY,
                    response_time=response_time,
                    message=f"Node Exporter returned HTTP {response.status_code}"
                )
                
        except requests.exceptions.ConnectionError:
            return HealthCheck(
                service=service,
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                message="Cannot connect to Node Exporter service"
            )
        except Exception as e:
            return HealthCheck(
                service=service,
                status=HealthStatus.UNKNOWN,
                response_time=time.time() - start_time,
                message=f"Error checking Node Exporter health: {str(e)}"
            )
    
    def check_cadvisor_health(self) -> HealthCheck:
        """Check cAdvisor service health"""
        service = "cadvisor"
        start_time = time.time()
        
        try:
            url = "http://localhost:8080/metrics"
            response = self.session.get(url)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                # Check if we're getting container metrics
                metrics_text = response.text
                if "container_" in metrics_text:
                    return HealthCheck(
                        service=service,
                        status=HealthStatus.HEALTHY,
                        response_time=response_time,
                        message="cAdvisor is healthy",
                        details={"metrics_size": len(metrics_text)}
                    )
                else:
                    return HealthCheck(
                        service=service,
                        status=HealthStatus.DEGRADED,
                        response_time=response_time,
                        message="cAdvisor is up but not returning expected metrics"
                    )
            else:
                return HealthCheck(
                    service=service,
                    status=HealthStatus.UNHEALTHY,
                    response_time=response_time,
                    message=f"cAdvisor returned HTTP {response.status_code}"
                )
                
        except requests.exceptions.ConnectionError:
            return HealthCheck(
                service=service,
                status=HealthStatus.UNHEALTHY,
                response_time=time.time() - start_time,
                message="Cannot connect to cAdvisor service"
            )
        except Exception as e:
            return HealthCheck(
                service=service,
                status=HealthStatus.UNKNOWN,
                response_time=time.time() - start_time,
                message=f"Error checking cAdvisor health: {str(e)}"
            )
    
    def check_all_services(self) -> List[HealthCheck]:
        """Check health of all monitoring services"""
        checks = []
        
        # Define all health check methods
        health_checks = [
            self.check_grafana_health,
            self.check_prometheus_health,
            self.check_node_exporter_health,
            self.check_cadvisor_health
        ]
        
        for check_method in health_checks:
            try:
                result = check_method()
                checks.append(result)
                logger.info(f"Health check for {result.service}: {result.status.value}")
            except Exception as e:
                logger.error(f"Failed to run health check {check_method.__name__}: {str(e)}")
        
        return checks
    
    def get_overall_health(self, checks: List[HealthCheck] = None) -> Dict[str, Any]:
        """Get overall health status of the monitoring infrastructure"""
        if checks is None:
            checks = self.check_all_services()
        
        # Count statuses
        status_counts = {
            HealthStatus.HEALTHY: 0,
            HealthStatus.UNHEALTHY: 0,
            HealthStatus.DEGRADED: 0,
            HealthStatus.UNKNOWN: 0
        }
        
        for check in checks:
            status_counts[check.status] += 1
        
        total_services = len(checks)
        healthy_services = status_counts[HealthStatus.HEALTHY]
        
        # Determine overall status
        if status_counts[HealthStatus.UNHEALTHY] > 0:
            overall_status = HealthStatus.UNHEALTHY
        elif status_counts[HealthStatus.DEGRADED] > 0:
            overall_status = HealthStatus.DEGRADED
        elif status_counts[HealthStatus.UNKNOWN] > 0:
            overall_status = HealthStatus.UNKNOWN
        else:
            overall_status = HealthStatus.HEALTHY
        
        # Calculate average response time
        avg_response_time = sum(check.response_time for check in checks) / len(checks) if checks else 0
        
        return {
            "overall_status": overall_status.value,
            "healthy_services": healthy_services,
            "total_services": total_services,
            "health_percentage": (healthy_services / total_services * 100) if total_services > 0 else 0,
            "average_response_time": avg_response_time,
            "status_breakdown": {status.value: count for status, count in status_counts.items()},
            "individual_checks": [
                {
                    "service": check.service,
                    "status": check.status.value,
                    "response_time": check.response_time,
                    "message": check.message,
                    "details": check.details,
                    "timestamp": check.timestamp
                }
                for check in checks
            ],
            "timestamp": time.time()
        }
    
    def wait_for_services(self, timeout: int = 300, check_interval: int = 5) -> bool:
        """Wait for all services to become healthy"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            checks = self.check_all_services()
            overall_health = self.get_overall_health(checks)
            
            if overall_health["overall_status"] == HealthStatus.HEALTHY.value:
                logger.info("All monitoring services are healthy")
                return True
            
            unhealthy_services = [
                check.service for check in checks 
                if check.status != HealthStatus.HEALTHY
            ]
            
            logger.info(f"Waiting for services to become healthy: {unhealthy_services}")
            time.sleep(check_interval)
        
        logger.error(f"Services did not become healthy within {timeout} seconds")
        return False


def main():
    """Main function for standalone health checking"""
    logging.basicConfig(level=logging.INFO)
    
    checker = HealthChecker()
    overall_health = checker.get_overall_health()
    
    print("=== HexStrike AI Monitoring Health Status ===")
    print(f"Overall Status: {overall_health['overall_status'].upper()}")
    print(f"Healthy Services: {overall_health['healthy_services']}/{overall_health['total_services']}")
    print(f"Health Percentage: {overall_health['health_percentage']:.1f}%")
    print(f"Average Response Time: {overall_health['average_response_time']:.3f}s")
    print()
    
    print("Individual Service Status:")
    for check in overall_health['individual_checks']:
        status_icon = "✅" if check['status'] == 'healthy' else "❌" if check['status'] == 'unhealthy' else "⚠️"
        print(f"  {status_icon} {check['service']}: {check['status']} ({check['response_time']:.3f}s)")
        if check['message']:
            print(f"    {check['message']}")


if __name__ == "__main__":
    main()