"""
Rate Limiter

This module provides rate limiting functionality for API endpoints.
"""

from flask import Flask, request, jsonify, g
from functools import wraps
import time
import logging
from collections import defaultdict, deque
from threading import Lock

logger = logging.getLogger(__name__)


class InMemoryRateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = defaultdict(deque)
        self.lock = Lock()
    
    def is_allowed(self, key: str, limit: int, window: int) -> tuple[bool, dict]:
        """
        Check if request is allowed under rate limit
        
        Args:
            key: Unique identifier for the client (IP, user ID, etc.)
            limit: Maximum number of requests allowed
            window: Time window in seconds
            
        Returns:
            Tuple of (is_allowed, rate_limit_info)
        """
        with self.lock:
            now = time.time()
            window_start = now - window
            
            # Clean old requests
            while self.requests[key] and self.requests[key][0] < window_start:
                self.requests[key].popleft()
            
            # Check if limit exceeded
            current_requests = len(self.requests[key])
            is_allowed = current_requests < limit
            
            if is_allowed:
                self.requests[key].append(now)
            
            # Calculate reset time
            if self.requests[key]:
                reset_time = int(self.requests[key][0] + window)
            else:
                reset_time = int(now + window)
            
            rate_limit_info = {
                'limit': limit,
                'remaining': max(0, limit - current_requests - (1 if is_allowed else 0)),
                'reset': reset_time,
                'retry_after': reset_time - int(now) if not is_allowed else None
            }
            
            return is_allowed, rate_limit_info


# Global rate limiter instance
rate_limiter = InMemoryRateLimiter()


def get_client_identifier():
    """Get unique identifier for the client"""
    # Try to get user ID from authentication
    user = getattr(g, 'current_user', None)
    if user:
        return f"user:{user.get('user_id')}"
    
    # Fall back to IP address
    return f"ip:{request.remote_addr}"


def rate_limit(limit: int = 100, window: int = 3600, per: str = "hour"):
    """
    Rate limiting decorator
    
    Args:
        limit: Maximum number of requests
        window: Time window in seconds (default 3600 for per="hour")
        per: Time period ("minute", "hour", "day") - overrides window if provided
    """
    
    # Convert per to seconds
    if per == "minute":
        window = 60
    elif per == "hour":
        window = 3600
    elif per == "day":
        window = 86400
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_id = get_client_identifier()
            
            is_allowed, rate_info = rate_limiter.is_allowed(client_id, limit, window)
            
            if not is_allowed:
                logger.warning(f"Rate limit exceeded for client {client_id}")
                
                response = jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Limit: {limit} per {per}',
                    'retry_after': rate_info['retry_after']
                })
                
                response.status_code = 429
                response.headers['X-Rate-Limit-Limit'] = str(rate_info['limit'])
                response.headers['X-Rate-Limit-Remaining'] = str(rate_info['remaining'])
                response.headers['X-Rate-Limit-Reset'] = str(rate_info['reset'])
                response.headers['Retry-After'] = str(rate_info['retry_after'])
                
                return response
            
            # Add rate limit headers to successful responses
            response = f(*args, **kwargs)
            
            if hasattr(response, 'headers'):
                response.headers['X-Rate-Limit-Limit'] = str(rate_info['limit'])
                response.headers['X-Rate-Limit-Remaining'] = str(rate_info['remaining'])
                response.headers['X-Rate-Limit-Reset'] = str(rate_info['reset'])
            
            return response
        
        return decorated_function
    return decorator


def setup_rate_limiting(app: Flask):
    """Setup global rate limiting for the Flask app"""
    
    # Global rate limiting configuration
    global_limit = app.config.get('RATE_LIMIT_GLOBAL', 1000)  # requests per hour
    global_window = app.config.get('RATE_LIMIT_WINDOW', 3600)  # 1 hour
    
    @app.before_request
    def global_rate_limit():
        """Apply global rate limiting to all requests"""
        
        # Skip rate limiting for certain endpoints
        exempt_endpoints = [
            '/health',
            '/api/auth/validate',
            '/static'
        ]
        
        if any(request.path.startswith(endpoint) for endpoint in exempt_endpoints):
            return
        
        client_id = get_client_identifier()
        is_allowed, rate_info = rate_limiter.is_allowed(
            f"global:{client_id}", 
            global_limit, 
            global_window
        )
        
        if not is_allowed:
            logger.warning(f"Global rate limit exceeded for client {client_id}")
            
            response = jsonify({
                'error': 'Global rate limit exceeded',
                'message': f'Too many requests. Global limit: {global_limit} per hour',
                'retry_after': rate_info['retry_after']
            })
            
            response.status_code = 429
            response.headers['X-Rate-Limit-Limit'] = str(rate_info['limit'])
            response.headers['X-Rate-Limit-Remaining'] = str(rate_info['remaining'])
            response.headers['X-Rate-Limit-Reset'] = str(rate_info['reset'])
            response.headers['Retry-After'] = str(rate_info['retry_after'])
            
            return response
    
    logger.info(f"Global rate limiting configured: {global_limit} requests per hour")


# Predefined rate limit decorators for common use cases
def rate_limit_strict(f):
    """Strict rate limiting: 10 requests per minute"""
    return rate_limit(limit=10, per="minute")(f)


def rate_limit_moderate(f):
    """Moderate rate limiting: 100 requests per hour"""
    return rate_limit(limit=100, per="hour")(f)


def rate_limit_generous(f):
    """Generous rate limiting: 1000 requests per hour"""
    return rate_limit(limit=1000, per="hour")(f)