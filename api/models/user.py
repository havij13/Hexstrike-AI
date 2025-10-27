"""
User Model

This module contains the User data model and related functionality.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import json


@dataclass
class User:
    """User data model"""
    id: str
    username: str
    email: str
    roles: List[str] = field(default_factory=list)
    tenant_id: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    status: str = "active"  # active, inactive, suspended
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    preferences: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'roles': self.roles,
            'tenant_id': self.tenant_id,
            'display_name': self.display_name,
            'avatar_url': self.avatar_url,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'preferences': self.preferences,
            'metadata': self.metadata
        }

    def to_public_dict(self) -> Dict[str, Any]:
        """Convert user to public dictionary (excluding sensitive data)"""
        return {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'avatar_url': self.avatar_url,
            'status': self.status,
            'roles': self.roles
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create User instance from dictionary"""
        return cls(
            id=data['id'],
            username=data['username'],
            email=data['email'],
            roles=data.get('roles', []),
            tenant_id=data.get('tenant_id'),
            display_name=data.get('display_name'),
            avatar_url=data.get('avatar_url'),
            status=data.get('status', 'active'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None,
            last_login=datetime.fromisoformat(data['last_login']) if data.get('last_login') else None,
            preferences=data.get('preferences', {}),
            metadata=data.get('metadata', {})
        )

    def has_role(self, role: str) -> bool:
        """Check if user has specific role"""
        return role in self.roles

    def has_any_role(self, roles: List[str]) -> bool:
        """Check if user has any of the specified roles"""
        return any(role in self.roles for role in roles)

    def is_admin(self) -> bool:
        """Check if user is admin"""
        return 'admin' in self.roles

    def is_active(self) -> bool:
        """Check if user is active"""
        return self.status == 'active'

    def can_access_tenant(self, tenant_id: str) -> bool:
        """Check if user can access specific tenant"""
        # Admin can access all tenants
        if self.is_admin():
            return True
        
        # Users can only access their own tenant
        return self.tenant_id == tenant_id

    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()

    def set_preference(self, key: str, value: Any):
        """Set user preference"""
        self.preferences[key] = value
        self.updated_at = datetime.utcnow()

    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get user preference"""
        return self.preferences.get(key, default)

    def add_metadata(self, key: str, value: Any):
        """Add metadata"""
        self.metadata[key] = value
        self.updated_at = datetime.utcnow()

    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata"""
        return self.metadata.get(key, default)


class UserSerializer:
    """User serializer for API responses"""

    @staticmethod
    def serialize(user: User, include_sensitive: bool = False) -> Dict[str, Any]:
        """Serialize user for API response"""
        if include_sensitive:
            return user.to_dict()
        else:
            return user.to_public_dict()

    @staticmethod
    def serialize_list(users: List[User], include_sensitive: bool = False) -> List[Dict[str, Any]]:
        """Serialize list of users for API response"""
        return [UserSerializer.serialize(user, include_sensitive) for user in users]

    @staticmethod
    def deserialize(data: Dict[str, Any]) -> User:
        """Deserialize user from API request"""
        return User.from_dict(data)