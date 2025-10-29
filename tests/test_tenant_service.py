"""
Tests for Tenant Service

This module contains unit tests for multi-tenant functionality.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from services.tenant_service import TenantService, Tenant, TenantResourceLimits


class TestTenantService:
    """Test cases for tenant service"""

    @pytest.fixture
    def tenant_service(self):
        """Create fresh tenant service for each test"""
        return TenantService()

    def test_initialization_creates_default_tenant(self, tenant_service):
        """Test that initialization creates default tenant"""
        default_tenant = tenant_service.get_tenant("default")
        
        assert default_tenant is not None
        assert default_tenant.id == "default"
        assert default_tenant.name == "Default Tenant"
        assert default_tenant.status == "active"

    def test_create_tenant_success(self, tenant_service):
        """Test successful tenant creation"""
        tenant = tenant_service.create_tenant(
            name="Test Company",
            domain="test.com",
            settings={"theme": "dark"},
            resource_limits={"max_users": 100}
        )
        
        assert tenant is not None
        assert tenant.name == "Test Company"
        assert tenant.domain == "test.com"
        assert tenant.status == "active"
        assert tenant.settings["theme"] == "dark"
        assert tenant.resource_limits["max_users"] == 100
        
        # Verify tenant is stored
        retrieved = tenant_service.get_tenant(tenant.id)
        assert retrieved == tenant

    def test_create_tenant_with_defaults(self, tenant_service):
        """Test tenant creation with default values"""
        tenant = tenant_service.create_tenant(name="Minimal Company")
        
        assert tenant.name == "Minimal Company"
        assert tenant.domain is None
        assert tenant.status == "active"
        assert "theme" in tenant.settings
        assert "max_users" in tenant.resource_limits

    def test_get_tenant_existing(self, tenant_service):
        """Test getting existing tenant"""
        created = tenant_service.create_tenant(name="Test Company")
        retrieved = tenant_service.get_tenant(created.id)
        
        assert retrieved == created

    def test_get_tenant_nonexistent(self, tenant_service):
        """Test getting non-existent tenant"""
        result = tenant_service.get_tenant("nonexistent")
        
        assert result is None

    def test_get_tenant_by_domain_existing(self, tenant_service):
        """Test getting tenant by domain"""
        created = tenant_service.create_tenant(name="Test Company", domain="test.com")
        retrieved = tenant_service.get_tenant_by_domain("test.com")
        
        assert retrieved == created

    def test_get_tenant_by_domain_nonexistent(self, tenant_service):
        """Test getting tenant by non-existent domain"""
        result = tenant_service.get_tenant_by_domain("nonexistent.com")
        
        assert result is None

    def test_list_tenants(self, tenant_service):
        """Test listing all tenants"""
        # Should have default tenant
        tenants = tenant_service.list_tenants()
        assert len(tenants) == 1
        assert tenants[0].id == "default"
        
        # Add more tenants
        tenant1 = tenant_service.create_tenant(name="Company 1")
        tenant2 = tenant_service.create_tenant(name="Company 2")
        
        tenants = tenant_service.list_tenants()
        assert len(tenants) == 3
        
        tenant_ids = [t.id for t in tenants]
        assert "default" in tenant_ids
        assert tenant1.id in tenant_ids
        assert tenant2.id in tenant_ids

    def test_update_tenant_success(self, tenant_service):
        """Test successful tenant update"""
        tenant = tenant_service.create_tenant(name="Original Name")
        original_updated_at = tenant.updated_at
        
        # Small delay to ensure updated_at changes
        import time
        time.sleep(0.01)
        
        updated = tenant_service.update_tenant(
            tenant.id,
            name="Updated Name",
            status="inactive",
            settings={"new_setting": "value"}
        )
        
        assert updated is not None
        assert updated.name == "Updated Name"
        assert updated.status == "inactive"
        assert updated.settings["new_setting"] == "value"
        assert updated.updated_at > original_updated_at

    def test_update_tenant_nonexistent(self, tenant_service):
        """Test updating non-existent tenant"""
        result = tenant_service.update_tenant("nonexistent", name="New Name")
        
        assert result is None

    def test_delete_tenant_success(self, tenant_service):
        """Test successful tenant deletion"""
        tenant = tenant_service.create_tenant(name="To Delete")
        
        result = tenant_service.delete_tenant(tenant.id)
        
        assert result is True
        assert tenant_service.get_tenant(tenant.id) is None

    def test_delete_tenant_default_forbidden(self, tenant_service):
        """Test that default tenant cannot be deleted"""
        with pytest.raises(ValueError, match="Cannot delete default tenant"):
            tenant_service.delete_tenant("default")

    def test_delete_tenant_nonexistent(self, tenant_service):
        """Test deleting non-existent tenant"""
        result = tenant_service.delete_tenant("nonexistent")
        
        assert result is False

    def test_check_resource_limit_within_limit(self, tenant_service):
        """Test resource limit checking within limit"""
        tenant = tenant_service.create_tenant(
            name="Test Company",
            resource_limits={"max_users": 100}
        )
        
        result = tenant_service.check_resource_limit(tenant.id, "max_users", 50)
        
        assert result is True

    def test_check_resource_limit_at_limit(self, tenant_service):
        """Test resource limit checking at limit"""
        tenant = tenant_service.create_tenant(
            name="Test Company",
            resource_limits={"max_users": 100}
        )
        
        result = tenant_service.check_resource_limit(tenant.id, "max_users", 100)
        
        assert result is False

    def test_check_resource_limit_over_limit(self, tenant_service):
        """Test resource limit checking over limit"""
        tenant = tenant_service.create_tenant(
            name="Test Company",
            resource_limits={"max_users": 100}
        )
        
        result = tenant_service.check_resource_limit(tenant.id, "max_users", 150)
        
        assert result is False

    def test_check_resource_limit_no_limit_set(self, tenant_service):
        """Test resource limit checking when no limit is set"""
        tenant = tenant_service.create_tenant(name="Test Company")
        
        # Remove the limit
        tenant.resource_limits.pop("max_users", None)
        
        result = tenant_service.check_resource_limit(tenant.id, "max_users", 1000)
        
        assert result is True

    def test_check_resource_limit_nonexistent_tenant(self, tenant_service):
        """Test resource limit checking for non-existent tenant"""
        result = tenant_service.check_resource_limit("nonexistent", "max_users", 50)
        
        assert result is False

    def test_get_resource_usage(self, tenant_service):
        """Test getting resource usage"""
        tenant = tenant_service.create_tenant(name="Test Company")
        
        usage = tenant_service.get_resource_usage(tenant.id)
        
        assert isinstance(usage, dict)
        assert "users" in usage
        assert "scans_today" in usage
        assert "concurrent_scans" in usage
        assert "storage_used_gb" in usage

    def test_is_tool_allowed_empty_list(self, tenant_service):
        """Test tool access when allowed_tools is empty (all allowed)"""
        tenant = tenant_service.create_tenant(
            name="Test Company",
            resource_limits={"allowed_tools": []}
        )
        
        result = tenant_service.is_tool_allowed(tenant.id, "nmap")
        
        assert result is True

    def test_is_tool_allowed_in_list(self, tenant_service):
        """Test tool access when tool is in allowed list"""
        tenant = tenant_service.create_tenant(
            name="Test Company",
            resource_limits={"allowed_tools": ["nmap", "nuclei"]}
        )
        
        result = tenant_service.is_tool_allowed(tenant.id, "nmap")
        
        assert result is True

    def test_is_tool_allowed_not_in_list(self, tenant_service):
        """Test tool access when tool is not in allowed list"""
        tenant = tenant_service.create_tenant(
            name="Test Company",
            resource_limits={"allowed_tools": ["nmap", "nuclei"]}
        )
        
        result = tenant_service.is_tool_allowed(tenant.id, "sqlmap")
        
        assert result is False

    def test_is_tool_allowed_nonexistent_tenant(self, tenant_service):
        """Test tool access for non-existent tenant"""
        result = tenant_service.is_tool_allowed("nonexistent", "nmap")
        
        assert result is False

    def test_get_tenant_settings(self, tenant_service):
        """Test getting tenant settings"""
        tenant = tenant_service.create_tenant(
            name="Test Company",
            settings={"theme": "dark", "notifications": True}
        )
        
        settings = tenant_service.get_tenant_settings(tenant.id)
        
        assert settings["theme"] == "dark"
        assert settings["notifications"] is True

    def test_get_tenant_settings_nonexistent(self, tenant_service):
        """Test getting settings for non-existent tenant"""
        settings = tenant_service.get_tenant_settings("nonexistent")
        
        assert settings == {}

    def test_update_tenant_settings_success(self, tenant_service):
        """Test updating tenant settings"""
        tenant = tenant_service.create_tenant(
            name="Test Company",
            settings={"theme": "light"}
        )
        
        result = tenant_service.update_tenant_settings(
            tenant.id,
            {"theme": "dark", "new_setting": "value"}
        )
        
        assert result is True
        
        updated_settings = tenant_service.get_tenant_settings(tenant.id)
        assert updated_settings["theme"] == "dark"
        assert updated_settings["new_setting"] == "value"

    def test_update_tenant_settings_nonexistent(self, tenant_service):
        """Test updating settings for non-existent tenant"""
        result = tenant_service.update_tenant_settings(
            "nonexistent",
            {"theme": "dark"}
        )
        
        assert result is False


class TestTenantResourceLimits:
    """Test cases for tenant resource limits data class"""

    def test_default_values(self):
        """Test default resource limit values"""
        limits = TenantResourceLimits()
        
        assert limits.max_users == 100
        assert limits.max_scans_per_day == 1000
        assert limits.max_concurrent_scans == 10
        assert limits.max_storage_gb == 100
        assert limits.allowed_tools is None
        assert limits.scan_timeout_minutes == 60

    def test_custom_values(self):
        """Test custom resource limit values"""
        limits = TenantResourceLimits(
            max_users=50,
            max_scans_per_day=500,
            allowed_tools=["nmap", "nuclei"]
        )
        
        assert limits.max_users == 50
        assert limits.max_scans_per_day == 500
        assert limits.allowed_tools == ["nmap", "nuclei"]


class TestTenantIntegration:
    """Integration tests for tenant functionality"""

    def test_multi_tenant_workflow(self):
        """Test complete multi-tenant workflow"""
        service = TenantService()
        
        # Create tenant
        tenant = service.create_tenant(
            name="Acme Corp",
            domain="acme.com",
            settings={"theme": "corporate"},
            resource_limits={"max_users": 50, "allowed_tools": ["nmap", "nuclei"]}
        )
        
        # Verify tenant creation
        assert tenant.name == "Acme Corp"
        assert service.get_tenant_by_domain("acme.com") == tenant
        
        # Check resource limits
        assert service.check_resource_limit(tenant.id, "max_users", 25) is True
        assert service.check_resource_limit(tenant.id, "max_users", 75) is False
        
        # Check tool access
        assert service.is_tool_allowed(tenant.id, "nmap") is True
        assert service.is_tool_allowed(tenant.id, "sqlmap") is False
        
        # Update settings
        service.update_tenant_settings(tenant.id, {"notifications": True})
        settings = service.get_tenant_settings(tenant.id)
        assert settings["notifications"] is True
        
        # Update tenant
        updated = service.update_tenant(tenant.id, status="inactive")
        assert updated.status == "inactive"
        
        # List tenants
        tenants = service.list_tenants()
        assert len(tenants) == 2  # default + acme
        
        # Delete tenant
        result = service.delete_tenant(tenant.id)
        assert result is True
        assert service.get_tenant(tenant.id) is None