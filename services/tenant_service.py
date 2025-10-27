"""
Tenant Management Service

This module provides multi-tenant functionality for HexStrike AI.
"""

from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


@dataclass
class Tenant:
    """Tenant data model"""
    id: str
    name: str
    domain: Optional[str]
    status: str
    settings: Dict[str, Any]
    resource_limits: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


@dataclass
class TenantResourceLimits:
    """Tenant resource limits"""
    max_users: int = 100
    max_scans_per_day: int = 1000
    max_concurrent_scans: int = 10
    max_storage_gb: int = 100
    allowed_tools: List[str] = None
    scan_timeout_minutes: int = 60


class TenantService:
    """Service for managing multi-tenant functionality"""
    
    def __init__(self):
        self.tenants: Dict[str, Tenant] = {}
        self._initialize_default_tenant()
    
    def _initialize_default_tenant(self):
        """Initialize default tenant for single-tenant deployments"""
        default_tenant = Tenant(
            id="default",
            name="Default Tenant",
            domain=None,
            status="active",
            settings={
                "theme": "dark",
                "timezone": "UTC",
                "notifications_enabled": True
            },
            resource_limits={
                "max_users": 1000,
                "max_scans_per_day": 10000,
                "max_concurrent_scans": 50,
                "max_storage_gb": 1000,
                "allowed_tools": [],  # Empty means all tools allowed
                "scan_timeout_minutes": 120
            },
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.tenants["default"] = default_tenant
    
    def create_tenant(self, name: str, domain: Optional[str] = None, 
                     settings: Optional[Dict[str, Any]] = None,
                     resource_limits: Optional[Dict[str, Any]] = None) -> Tenant:
        """Create a new tenant"""
        try:
            tenant_id = str(uuid.uuid4())
            
            # Default settings
            default_settings = {
                "theme": "light",
                "timezone": "UTC",
                "notifications_enabled": True,
                "webhook_enabled": False
            }
            
            # Default resource limits
            default_limits = {
                "max_users": 50,
                "max_scans_per_day": 500,
                "max_concurrent_scans": 5,
                "max_storage_gb": 50,
                "allowed_tools": [],
                "scan_timeout_minutes": 60
            }
            
            # Merge with provided settings
            if settings:
                default_settings.update(settings)
            if resource_limits:
                default_limits.update(resource_limits)
            
            tenant = Tenant(
                id=tenant_id,
                name=name,
                domain=domain,
                status="active",
                settings=default_settings,
                resource_limits=default_limits,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.tenants[tenant_id] = tenant
            
            logger.info(f"Created tenant: {name} (ID: {tenant_id})")
            return tenant
            
        except Exception as e:
            logger.error(f"Error creating tenant: {str(e)}")
            raise
    
    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        """Get tenant by ID"""
        return self.tenants.get(tenant_id)
    
    def get_tenant_by_domain(self, domain: str) -> Optional[Tenant]:
        """Get tenant by domain"""
        for tenant in self.tenants.values():
            if tenant.domain == domain:
                return tenant
        return None
    
    def list_tenants(self) -> List[Tenant]:
        """List all tenants"""
        return list(self.tenants.values())
    
    def update_tenant(self, tenant_id: str, **kwargs) -> Optional[Tenant]:
        """Update tenant"""
        try:
            tenant = self.tenants.get(tenant_id)
            if not tenant:
                return None
            
            # Update allowed fields
            if 'name' in kwargs:
                tenant.name = kwargs['name']
            if 'domain' in kwargs:
                tenant.domain = kwargs['domain']
            if 'status' in kwargs:
                tenant.status = kwargs['status']
            if 'settings' in kwargs:
                tenant.settings.update(kwargs['settings'])
            if 'resource_limits' in kwargs:
                tenant.resource_limits.update(kwargs['resource_limits'])
            
            tenant.updated_at = datetime.utcnow()
            
            logger.info(f"Updated tenant: {tenant_id}")
            return tenant
            
        except Exception as e:
            logger.error(f"Error updating tenant {tenant_id}: {str(e)}")
            raise
    
    def delete_tenant(self, tenant_id: str) -> bool:
        """Delete tenant"""
        try:
            if tenant_id == "default":
                raise ValueError("Cannot delete default tenant")
            
            if tenant_id in self.tenants:
                del self.tenants[tenant_id]
                logger.info(f"Deleted tenant: {tenant_id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error deleting tenant {tenant_id}: {str(e)}")
            raise
    
    def check_resource_limit(self, tenant_id: str, resource: str, current_usage: int) -> bool:
        """Check if tenant is within resource limits"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return False
        
        limit = tenant.resource_limits.get(resource)
        if limit is None:
            return True  # No limit set
        
        return current_usage < limit
    
    def get_resource_usage(self, tenant_id: str) -> Dict[str, Any]:
        """Get current resource usage for tenant"""
        # In real implementation, this would query the database
        # For now, return mock data
        return {
            "users": 15,
            "scans_today": 45,
            "concurrent_scans": 2,
            "storage_used_gb": 12.5,
            "tools_used": ["nmap", "nuclei", "gobuster"]
        }
    
    def is_tool_allowed(self, tenant_id: str, tool_name: str) -> bool:
        """Check if tool is allowed for tenant"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return False
        
        allowed_tools = tenant.resource_limits.get("allowed_tools", [])
        
        # Empty list means all tools are allowed
        if not allowed_tools:
            return True
        
        return tool_name in allowed_tools
    
    def get_tenant_settings(self, tenant_id: str) -> Dict[str, Any]:
        """Get tenant settings"""
        tenant = self.get_tenant(tenant_id)
        if not tenant:
            return {}
        
        return tenant.settings
    
    def update_tenant_settings(self, tenant_id: str, settings: Dict[str, Any]) -> bool:
        """Update tenant settings"""
        try:
            tenant = self.get_tenant(tenant_id)
            if not tenant:
                return False
            
            tenant.settings.update(settings)
            tenant.updated_at = datetime.utcnow()
            
            logger.info(f"Updated settings for tenant: {tenant_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating tenant settings {tenant_id}: {str(e)}")
            return False


# Global tenant service instance
tenant_service = TenantService()